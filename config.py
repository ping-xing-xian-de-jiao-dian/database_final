from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 创建项目对象
app = Flask(__name__)

# SQLALCHEMY_DATABASE_URI:用于连接数据库
# mysql://username:password@hostname/database?编码
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "mysql+pymysql://root:12345@localhost:3306/internet_ordering_meals?charset=utf8mb4"

# 如果设置成True(默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
# 这需要额外的内存， 如果不必要的可以禁用它。如果你不显示的调用它，
# 在最新版的运行环境下，会显示警告。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_AS_ASCII = False

db = SQLAlchemy(app)


db.create_all()
