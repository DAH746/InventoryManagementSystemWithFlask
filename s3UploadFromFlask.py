from flask import Flask, render_template, request
import sqlite3 as sql
import random
import boto3
import string
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

s3 = boto3.client('s3')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BUCKET_NAME = 'source-image-bucket-5623'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/s3UploadTest')
def s3_upload():
    return render_template('s3UploadTest.html')

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            fileNameSplit = filename.split(".")
            fileExtention = fileNameSplit[1]
            if fileExtention in ALLOWED_EXTENSIONS:
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "
            else:
                msg = "Not a png/jpg/jpeg."

    return render_template("result.html",msg =msg)

if __name__ == '__main__':
   app.run(debug = True)