from flask import Flask , render_template ,request, jsonify,redirect,url_for

from keras.models import load_model, Model
from keras.preprocessing.image import load_img, img_to_array

import numpy as np
import os
import pymysql

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = "/static/images"


connect = pymysql.connect("localhost", "root", "12345678", "oramentalfishdb")

@app.route("/")
def home():
    with connect.cursor() as cursor:
        cur = connect.cursor() 
        cur.execute("select * from fishdb where No = '1'")
        rows = cur.fetchall()
        return render_template("index.html",datas = rows)
    
@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if request.files:
            file = request.files["image"]
            filepath = "./static/images/image.jpg"
            file.save(filepath)
    return redirect(url_for('showData'))

@app.route("/fishclassification_search")
def fishclassification_search():
    return render_template("fishclassification.html")

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

if __name__ == "__main__":
    model = load_model("model.h5")
    app.run(debug=True)