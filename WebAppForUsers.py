from flask import Flask, render_template, request
import sqlite3 as sql
import random
import string
from datetime import datetime

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
    return render_template("newuser.html")

@app.route('/adduser',methods = ['POST', 'GET'])
def add_user():
    if request.method =="POST":
        try:
            user_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
            email = request.form['email']
            print((type(email)))
            
            fn = request.form['fn']
            ln = request.form['ln']
            pword = request.form['pword']
            addr = request.form['addr']
            city = request.form['city']

            checkIfUserIsNew = IsUserNew(email)
            date_joined = datetime.now()
            if checkIfUserIsNew: 
                with sql.connect("UserDatabase.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO Users (user_id,email,first_name,last_name,pword,date_joined,address,city) VALUES (?,?,?,?,?,?,?,?)",(user_id,email,fn,ln,pword,date_joined,addr,city) )
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
                else:
                    msg = "Unsuccessful Login"

        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("result.html",msg = msg)
            con.close()


if __name__ == '__main__':
   app.run(debug = True)