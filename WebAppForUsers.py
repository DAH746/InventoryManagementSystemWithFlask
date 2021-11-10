from flask import Flask, render_template, request, url_for
import sqlite3 as sql
import random
import string
from datetime import datetime
import boto3
from werkzeug.utils import secure_filename
import s3_bucket_operations

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
- boto3
- secure_filename
Using  a user database and flask, creates a program to add users with several bits of info such as:
user_id, enail, first and last name, password and address details
Checks to see if the email already exists in the database.
Allows user to list all users for debugging purposes
Includes login function where the the user and upload picture to an S3 bucket to be resized
New product database. Allows user to add new products (checks to see if the product has already been added)
and then saves to database. User can also list all products in the database.
"""

app = Flask(__name__, template_folder='templates') #Sets the templates folder for the website
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # Sets maximum filesize to be uploaded at 1MB


s3 = boto3.client('s3') # Sets up S3 client
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Only allowed extensions allowed for file upload
BUCKET_NAME = 'source-image-bucket-5623'
# global LOGIN # Global login variable


# Function checks if the email inputted from the user is currently in the database.
# Queries the user database by selecting emails where the saved email is the same as the user
# input email. Returns True is user is new or False if already registered user.
def IsUserNew(email):
    con = sql.connect("UserDatabase.db") # The database to connect to
    cur = con.cursor()
    cur.execute("Select email from Users WHERE email=?",(email, )) # Queries database
    all_emails = cur.fetchall(); # Fetches output from query
    if len(all_emails) != 0: 
    # Checks if the output of query is not 0. If it's not 0 that means the query has found a match
    # and therefore the email has been used already, i.e. exisiting user.
        return False
    return True

# Home page for website
# Returns the home.html template which allows the user to use the functions in the website.
@app.route('/')
def home():
    return render_template('home.html')

# Called when the user wants to add a new user
# Returns the newuser.html template with the iput form required for getting the data from the user.
# Includes a role for who they are, depending on the role, they can use different functions.
@app.route('/enternewuser')
def new_user():
    roles = ['Warehouse', 'Authenticator', 'Customer']
    return render_template("newuser.html", roles=roles)

# newuser.html routes the form to this function
# Organises the data inputted from user for inserting to user database
@app.route('/adduser',methods = ['POST', 'GET'])
def add_user():
    if request.method =="POST":
        try:
            # Creates user_id using random characters
            user_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
            # Fetches information from html form
            email = request.form['email']
            fn = request.form['fn']
            ln = request.form['ln']
            pword = request.form['pword']
            addr = request.form['addr']
            city = request.form['city']
            role = request.form['role']

            # Checks if the user is new
            checkIfUserIsNew = IsUserNew(email)
            date_joined = datetime.now()
            if checkIfUserIsNew: # If user is new then will add user details to database
                with sql.connect("UserDatabase.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO Users (user_id,email,first_name,last_name,pword,date_joined,address,city,role) VALUES (?,?,?,?,?,?,?,?,?)",(user_id,email,fn,ln,pword,date_joined,addr,city,role) )
                    con.commit()
                    msg = "Record successfully added"
            # This executes if user is not new
            if not checkIfUserIsNew:
                msg = "This is an exsiting user"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            # Outputs the result of the operation
            # 1 of 3 options: Successfully add, not added due to existing user or error
            # Correct message will display depending on which of the 3 options happens
            return render_template("result.html",msg = msg)
            con.close()

# Lists the users in the database
# For debugging, will not be in the final website
@app.route('/list')
def list_users():
    con = sql.connect("UserDatabase.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Users")

    rows = cur.fetchall();
    return render_template("list.html", rows = rows)

# USer login page, calls the check_user_login function
@app.route('/UserLogin')
def user_login():
    return render_template('UserLogin.html')


# Checks if the users details entered are correct. If the email and password match for the same user then they are logged in succesfully
@app.route('/login',methods = ['POST'])
def check_user_login():
    global LOGIN
    if request.method =="POST":
        try:
            # Gets the information from the user
            email = request.form['email']
            pword = request.form['pword']
            with sql.connect("UserDatabase.db") as con:
                cur = con.cursor()
                # Selects the user where email and password match
                cur.execute("Select * from Users WHERE email=? AND pword=?", (email, pword, ))
                user_info = cur.fetchall();
                # If len(user_info) = 1, this means the query has found a user and therefore the user is logged in
                if len(user_info) == 1:
                    # User is told they are logged in
                    msg = "Successful Login"
                    # Sets the global variable, therefore allowing this to be seen later on
                    LOGIN = True 
                else:
                    # If anything else is found then the login is unsucessful and so the user is told
                    msg = "Unsuccessful Login"
                    LOGIN = False
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return (render_template("result.html",msg = msg))
            con.close()

# Checks if the user is logged in and therefore allowed to upload a picture to the s3 bucket
@app.route('/s3UploadTest')
def s3_upload():
    global LOGIN
    print("----------yoyoyoyo------------")
    print(LOGIN)
    
    if LOGIN: # Checks if LOGIN is true and then allows the user to upload the file
        return render_template('s3UploadTest.html')
    else:
        msg = "Please login first" # If LOGIN is false, the user is asked to login
        return render_template("result.html",msg = msg)

# Uploads the file to the s3 bucket
@app.route('/upload',methods=['post'])
def upload():
    global prod_id
    if request.method == 'POST':
        img = request.files['file'] # Takes the file, in this case apicture
        if img:
            filename = secure_filename(img.filename) # Gets the file name for the picture
            fileNameSplit = filename.split(".") # Splits the filename to get the extension
            fileExtention = fileNameSplit[1]
            if fileExtention in ALLOWED_EXTENSIONS: # Checks if the extensions are in the allowed extensions
                filename = prod_id + "." + fileExtention
                img.save(filename)
                # Uploads the file to the s3 bucket
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! " # Tells the user the upload is complete
            else:
                msg = "Not a png/jpg/jpeg." # Error occurs if the extension is not an allowed extension and tells the user this

    return render_template("result.html",msg =msg)

# For adding new products to inventory
@app.route('/newproduct')
def new_product():
    # For the drop down menu if the item is authenticated or not
    authenticated = ['Yes', 'No']
    return render_template("newproduct.html", authenticated=authenticated)

# Using the product id, the product is checked to see if it already exists
def IsProdNew(prod_id):
    con = sql.connect("InventoryDatabase.db") # Connects to the inventory Database
    cur = con.cursor()
    cur.execute("Select prod_id from Inventory WHERE prod_id=?",(prod_id, )) # Selects the products that have the same ID as the one given
    all_prod_id = cur.fetchall();
    if len(all_prod_id) != 0: # If there are some clashes the new product is not added
        return False
    return True

# Gets the information for the new product from the user via form
@app.route('/addproduct',methods = ['POST', 'GET'])
def add_product():
    global prod_id
    if request.method =="POST":
        try:

            prod_id = request.form['prod_ID']
            prod_name = request.form['prod_name']
            price = request.form['price']
            desc = request.form['desc']
            quantity = request.form['quantity']
            auth = request.form['auth']

            checkIfProdIsNew = IsProdNew(prod_id) # Checks if the product is new or exisiting

            if checkIfProdIsNew: 
                with sql.connect("InventoryDatabase.db") as con:
                    cur = con.cursor()
                    # Inserts the new product into the database
                    cur.execute("INSERT INTO Inventory (prod_ID,prod_name,price,desc,quantity,auth) VALUES (?,?,?,?,?,?)",(prod_id,prod_name,price,desc,quantity,auth) )
                    con.commit()
                    msg = "Product successfully added" # Tells the user the outcome

            if not checkIfProdIsNew: # If the product id is already there, the user will be told and the product is not added
                msg = "This is an exsiting product"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("s3UploadTest.html",msg = msg)
            con.close()

# List the products from the database for the users to see
@app.route('/listprods')
def list_prods():
    con = sql.connect("InventoryDatabase.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Inventory")

    rows = cur.fetchall();
    return render_template("listprods.html", rows = rows)

@app.route('/devTest')
# Show future version of what our home page will be
def devTest():

    # START - Dev test stuff
    s3_bucket_operations.getFileNamesOfObjectsWithinAnS3Bucket(getFromSourceBucket=False)

    s3_bucket_operations.getURLsOfAnObjectWithinAnS3Bucket(nameOfS3BucketToBeCalled="source-image-bucket-5623",
                                                           nameOfObjectFile="beach.jpg")
    # END - Dev test stuff

    return render_template('futureHomePage.html') # todo keep this here

@app.route('/dispImage')
def disp_image():
    return render_template('displayImage.html')



if __name__ == '__main__':
    # global LOGIN
    global LOGIN, prod_id
    LOGIN = False
    app.run(debug = True) # Starts the app in debug mode