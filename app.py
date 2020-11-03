from flask import Flask ,flash, render_template ,request, jsonify,redirect,url_for , session ,g

from keras.models import load_model, Model
from keras.preprocessing.image import load_img, img_to_array

from passlib.hash import sha256_crypt

import numpy as np
import os
import pymysql

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = "/static/images"


connect = pymysql.connect("localhost", "root", "12345678", "oramentalfishdb")
################################################
@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route("/dropsession")
def dropsession():
    session.pop('user',None)
    return redirect(url_for('home'))

################################################
@app.route("/")
def home():
    if g.user:
        return render_template("home.html",user = session['user'])
    else:
        with connect.cursor() as cursor:
            cur = connect.cursor() 
            cur.execute("select * from fishdb where No = '1'")
            rows = cur.fetchall()
            return render_template("index.html",datas = rows)
################################################    
@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if request.files:
            file = request.files["image"]
            filepath = "./static/images/image.jpg"
            file.save(filepath)
    return redirect(url_for('showData'))
################################################
@app.route("/fishclassification_search")
def fishclassification_search():
    if g.user:
        return render_template("fishclassification_login.html",user = session['user'])
    else:
        return render_template("fishclassification.html")
################################################
@app.route("/register" , methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        surname = request.form.get("surname")
        address = request.form.get("address")
        email = request.form.get("email")
        phone = request.form.get("phone")
        store_name = request.form.get("Store_name")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == password_confirm:
            with connect.cursor() as cursor:
                cur = connect.cursor() 
                cur.execute("INSERT INTO seller(Seller_Name,Seller_Last,Address,Phone_Number,Email,Password,Store_Name) VALUES(%s,%s,%s,%s,%s,%s,%s)" , (username,surname,address,phone,email,secure_password,store_name))
                connect.commit()
                return redirect(url_for("login"))
        else:
            flash("password does not match","danger")
            return render_template("register.html")    
    return render_template("register.html")
################################################
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        session.pop('user',None)
        
        email = request.form.get("email")
        password = request.form.get("password")
        with connect.cursor() as cursor:    
            cur = connect.cursor() 
            cur.execute("SELECT * FROM seller WHERE Email = %s" , (email))
            get_user = cur.fetchall() 
            if not get_user:
                flash("Login Fail","danger")
            else:
                get_password = get_user[0][5]
                if(sha256_crypt.verify(password, get_password)):
                    session['user'] = request.form['email']
                    return redirect(url_for('home'))
                    flash("Login success","success")
                else:
                    flash("incorrect Email or Password","warning")
    return render_template("login.html")
################################################
@app.route("/now_login")
def now_login():
    if g.user:
        return render_template("home.html", user = session['user'])
################################################
@app.route("/showData")
def showData():
    #loadimage, resize, to array
    img = load_img("./static/images/image.jpg", target_size = (300, 300))    
    img = img_to_array(img)        
    img = img.reshape(1, 300, 300, 3)
    img = img.astype('uint8')
    result = model.predict(img)
    predict_result = np.argmax(result[0])
    with connect.cursor() as cursor:
        cur = connect.cursor() 
        pos = str(predict_result)
        cur.execute("select * from fishdb where No = "+ pos)
        rows = cur.fetchall()
    return render_template("result.html", predict_result = rows)
################################################
if __name__ == "__main__":
    app.secret_key = "fhu1234567803102541fhu"
    model = load_model("model.h5")
    app.run(debug=True)
################################################