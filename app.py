from flask import Flask, render_template, request, url_for, redirect
import config, pymysql
# -*- coding:UTF-8 -*-
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.secret_key = '19281081'
app.config.from_object(config)


'''连接，增删改查类'''
class Connection:
    cols = ('菜名', '折扣', '价格')
    def connect(self, nm, pw):
        try:
            global con, cur, results
            con = pymysql.connect(user=nm, password=pw, db="internet_ordering_meals")
            con.autocommit(True)
            cur = con.cursor()
            cur.execute("select * from menu")
            results = cur.fetchall()
        except:
            return -1

    def delete(self):
        name = request.args.get('name')
        sql = "delete from menu where 菜名=" + "'" + name + "'"
        cur.execute(sql)

    def add(self):
        name = request.form['name']
        discount = request.form['discount']
        price = request.form['price']
        sql = "insert into menu(菜名,折扣,价格) values(" + "'" + name + "'," + discount + "," + price + ")"
        cur.execute(sql)

    def mod(self):
        name = request.form['name']
        discount = request.form['discount']
        price = request.form['price']
        sql = "update menu set 折扣=" + discount + ", 价格=" + price + " where 菜名='" + name + "'"
        cur.execute(sql)

    def sel(self):
        global results
        name = request.form['select']
        if name == "":
            cur.execute("select * from menu")
        else:
            cur.execute("select * from menu where 菜名 like '%" + name + "%'")
        results = cur.fetchall()
        return name


db = Connection
user_name = ""
user_password = ""


'''菜单'''
me_results = None
me_col = None
@app.route('/menu', methods=['POST', 'GET'])
def menu():
    global user_name, user_password
    if request.method == 'POST':
        user_name = request.form['nm']
        user_password = request.form['pw']
        # 声明类
    global db
    db = Connection()
    if -1 == db.connect(user_name, user_password):
        return '数据库用户名或密码错误，请重新输入！'
    else:
        cur.execute("select * from me")
        global me_results, me_col
        me_results = cur.fetchall()
        me_col = ('菜名', '份数', '价格')
        s = 0
        for row in me_results:
            s += row[2]
        return render_template('menu.html', cols = db.cols, res = results,
                                            me_cols = me_col, me_res = me_results,
                                            sum = s)


'''meReset'''
@app.route('/meReset')
def meReset():
    cur.execute("call delete_me_all")
    return redirect(url_for('menu'))

'''meFastAdd'''
@app.route('/meFastAdd')
def meFastAdd():
    cur.execute("call insert_me_fast_lunch")
    return redirect(url_for('menu'))

'''meDis'''
@app.route('/meDis')
def meDis():
    global cur
    cur.execute("call select_discount_products")
    temp_res = cur.fetchall()
    s = 0
    for row in me_results:
        s += row[2]
    return render_template('/menu.html', cols=db.cols, res=temp_res,
                                         me_cols=me_col, me_res=me_results,
                                         sum=s)

'''meUpd'''
@app.route('/meUpd')
def meUpd():
    global cur
    cur.execute("call update_me_allprices")
    return redirect(url_for('menu'))


'''meDel'''
@app.route('/meDel', methods=['POST', 'GET'])
def meDel():
    name = request.args.get('name')
    sql = "delete from me where 菜名=" + "'" + name + "'"
    cur.execute(sql)
    return redirect(url_for('menu'))

'''meModForm'''
@app.route('/meModForm/<name>/', methods=['POST', 'GET'])
def meModForm(name):
    return render_template('meModForm.html', nm = name)
@app.route('/meMod', methods=['POST', 'GET'])
def meMod():
    global cur
    name = request.form['name']
    num = request.form['num']
    sql = "update me set 份数=" + str(num) + " where 菜名='" + name + "'"
    cur.execute(sql)
    return redirect(url_for('meUpd'))


'''meAddForm'''
@app.route('/meAddForm', methods=['POST', 'GET'])
def meAddForm():
    return render_template('meAddForm.html')
@app.route('/meAdd', methods=['POST', 'GET'])
def meAdd():
    global cur
    name = request.form['name']
    num = request.form['num']
    sql = "insert into me(菜名,份数,价格) values(" + "'" + name + "'," + num + "," + str(0) + ")"
    cur.execute(sql)
    return redirect(url_for('meUpd'))





'''提交界面'''
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    global me_results, me_col
    s = 0
    for row in me_results:
        s += row[2]
    return render_template('submit.html', me_res=me_results, me_cols = me_col,
                                          sum=s)


'''订单配送界面'''
@app.route('/transmit')
def transmit():
    return render_template('transmit.html')

'''配送完成界面'''
@app.route('/complete')
def complete():
    return render_template('complete.html')




'''删除'''
@app.route('/menuDel', methods=['POST', 'GET'])
def menuDel():
    global db
    db.delete()
    return redirect(url_for('menu'))


'''增加'''
@app.route('/menuAddForm', methods=['POST', 'GET'])
def menuAddForm():
    return render_template('menuAddForm.html')
@app.route('/menuAdd', methods=['POST', 'GET'])
def menuAdd():
    global db
    db.add()
    return redirect(url_for('menu'))


'''修改'''
@app.route('/menuModForm/<name>/', methods=['POST', 'GET'])
def menuModForm(name):
    return render_template('menuModForm.html', nm = name)
@app.route('/menuMod', methods=['POST', 'GET'])
def menuMod():
    global db
    db.mod()
    return redirect(url_for('menu'))


'''查询'''
@app.route('/menuSel', methods=['POST', 'GET'])
def menuSel():
    global db, results
    if db.sel() == "":
        return redirect('menu')
    s = 0
    for row in me_results:
        s += row[2]
    return render_template('menu.html', cols = db.cols, res = results,
                                        me_cols = me_col, me_res = me_results,
                                        sum = s)


'''登录'''
@app.route('/')
def root():
    return render_template('log_in.html')



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
