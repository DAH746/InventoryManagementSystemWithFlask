from flask import Flask, redirect, url_for, render_template, request, flash

app = Flask(__name__)

# Selects the page for which a function is to be defined. Right now there will only be one page in your website.

@app.route('/')
def hello():

    return "<h1>Hello World!</h1>" \
           "\nThis is my introduction to Flask!" \
           "\nI can write a lot of things on this page.\nLet's get started!"

# The above function returns the HTML code to be displayed on the page

@app.route('/login')
def loginPage():
    return render_template('SignIn.html')

@app.route('/login_data', methods = ['GET', 'POST'])
def logintest():
    print("----------------------------------------> yoyoyo")
    data = request.form['user_login_data']
    print(data)
    return None

if __name__ == '__main__':

   app.run()