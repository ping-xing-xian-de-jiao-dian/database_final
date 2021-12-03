function plus(id, price, discount){
    document.getElementById(id).value++;
    var temp = parseFloat(document.getElementById('totPrice').value) + price * discount;
    temp = Math.floor(temp * 100) / 100;
    document.getElementById('totPrice').value = temp;
}

function minus(id, price, discount){
    if (document.getElementById(id).value > "0"){
        document.getElementById(id).value--;
        var temp = parseFloat(document.getElementById('totPrice').value) - price * discount;
        if (temp < 0) temp = 0;
        temp = Math.floor(temp * 100) / 100;
        document.getElementById('totPrice').value = temp;
    }
}