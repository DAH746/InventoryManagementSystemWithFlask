from flask import Flask, render_template, request
import sqlite3 as sql
import random
import string
from datetime import datetime
import boto3
from werkzeug.utils import secure_filename

"""
Importing serveral packages
- Flask
    - Flask
    - render_template
    - request
- sqlite
- random
- string
- datetime

Using database and flask, creates a program to add users with several bits of info such as:
user_id, enail, first and last name, password and address details

Checks to see if the email already exists in the database.

Allows user to list all users for debugging purposes

"""

app = Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

s3 = boto3.client('s3')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BUCKET_NAME = 'source-image-bucket-5623'
global LOGIN
LOGIN = False

def IsUserNew(email):
    con = sql.connect("UserDatabase.db")
    cur = con.cursor()
    cur.execute("Select email from Users WHERE email=?",(email, ))
    all_emails = cur.fetchall();
    if len(all_emails) != 0:
        return False
    return True


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternewuser')
def new_user():
    roles = ['Warehouse', 'Authenticator', 'Customer']
    return render_template("newuser.html", roles=roles)

@app.route('/adduser',methods = ['POST', 'GET'])
def add_user():
    if request.method =="POST":
        try:
            
            user_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
            email = request.form['email']
            fn = request.form['fn']
            ln = request.form['ln']
            pword = request.form['pword']
            addr = request.form['addr']
            city = request.form['city']
            role = request.form['role']

            checkIfUserIsNew = IsUserNew(email)
            date_joined = datetime.now()
            if checkIfUserIsNew: 
                with sql.connect("UserDatabase.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO Users (user_id,email,first_name,last_name,pword,date_joined,address,city,role) VALUES (?,?,?,?,?,?,?,?,?)",(user_id,email,fn,ln,pword,date_joined,addr,city,role) )
                    con.commit()
                    msg = "Record successfully added"

            if not checkIfUserIsNew:
                msg = "This is an exsiting user"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("result.html",msg = msg)
            con.close()

@app.route('/list')
def list_users():
    con = sql.connect("UserDatabase.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Users")

    rows = cur.fetchall();
    return render_template("list.html", rows = rows)


@app.route('/UserLogin')
def user_login():
    return render_template('UserLogin.html')

@app.route('/login',methods = ['POST'])
def check_user_login():
    if request.method =="POST":
        try:
            email = request.form['email']
            pword = request.form['pword']
            with sql.connect("UserDatabase.db") as con:
                cur = con.cursor()
                cur.execute("Select * from Users WHERE email=? AND pword=?", (email, pword, ))
                user_info = cur.fetchall();
                if len(user_info) == 1:
                    msg = "Successful Login"
                    global LOGIN
                    LOGIN = True 
                else:
                    msg = "Unsuccessful Login"
                    LOGIN = False

        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("result.html",msg = msg)
            con.close()

@app.route('/s3UploadTest')
def s3_upload():
    if LOGIN:
        return render_template('s3UploadTest.html')
    else:
        msg = "Please login first"
        return render_template("result.html",msg = msg)

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

@app.route('/newproduct')
def new_product():
    authenticated = ['Yes', 'No']
    return render_template("newproduct.html", authenticated=authenticated)

def IsProdNew(prod_id):
    con = sql.connect("InventoryDatabase.db")
    cur = con.cursor()
    cur.execute("Select prod_id from Inventory WHERE prod_id=?",(prod_id, ))
    all_prod_id = cur.fetchall();
    if len(all_prod_id) != 0:
        return False
    return True

@app.route('/addproduct',methods = ['POST', 'GET'])
def add_product():
    if request.method =="POST":
        try:
            
            prod_id = request.form['prod_ID']
            prod_name = request.form['prod_name']
            desc = request.form['desc']
            quantity = request.form['quantity']
            auth = request.form['auth']
            pic_id = request.form['pic_id']
            
            checkIfProdIsNew = IsProdNew(prod_id)

            if checkIfProdIsNew: 
                with sql.connect("InventoryDatabase.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO Inventory (prod_ID,prod_name,desc,quantity,auth,pic_id) VALUES (?,?,?,?,?,?)",(prod_id,prod_name,desc,quantity,auth,pic_id) )
                    con.commit()
                    msg = "Product successfully added"

            if not checkIfProdIsNew:
                msg = "This is an exsiting user"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("result.html",msg = msg)
            con.close()

@app.route('/listprods')
def list_prods():
    con = sql.connect("InventoryDatabase.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Inventory")

    rows = cur.fetchall();
    return render_template("listprods.html", rows = rows)

if __name__ == '__main__':
   app.run(debug = True)