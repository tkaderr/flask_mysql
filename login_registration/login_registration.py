from flask import Flask, redirect, request, render_template, session, flash
from mysqlconnection import  MySQLConnector
import re

app=Flask(__name__)
app.secret_key=("secret_key")

mysql=MySQLConnector(app,"emaildb")
FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
LAST_NAME_REGEX =re.compile(r'^[a-zA-Z]*$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def registration_page():
    return render_template("registration.html")

@app.route('/success')
def logged():
    return render_template("submitted_form.html")

@app.route('/login', methods=["POST"])
def user_login():
    email_name=str(request.form["email_name"])
    password=str(request.form["password"])
    query1 = "SELECT * FROM user_emails WHERE email=:email LIMIT 1"
    data_email= {
        "email": request.form["email_name"]
        }
    email_check=mysql.query_db(query1,data_email)
    if not email_check:
        flash("Email or password incorrect")
        return redirect('/')
    query2 = "SELECT * FROM user_emails WHERE password=:password and email=:email LIMIT 1"
    data_password= {
        "email": request.form["email_name"],
        "password": request.form["password"]
        }
    password_check=mysql.query_db(query2,data_password)
    if not password_check:
        flash("Password is wrong")
        return redirect('/')
    return redirect('/success')

@app.route('/register', methods=["POST"])
def user_register():
    first_name=str(request.form["first_name"])
    last_name=str(request.form["last_name"])
    email_name=str(request.form["email_name"])
    password=str(request.form["password"])
    confirm_password=str(request.form["confirm_password"])
    query = "SELECT email FROM user_emails WHERE email=:email"
    data_email= {
        "email": request.form["email_name"]
        }
    email_check=mysql.query_db(query,data_email)

    if len(first_name)<2 or not FIRST_NAME_REGEX.match(first_name) or str.isalpha(first_name) != True:
        flash("The first name is too short and invalid letters")
        return redirect('/')
    else:
        session["first_name"]=first_name
    if len(last_name)<2 or not LAST_NAME_REGEX.match(first_name) or str.isalpha(last_name)!=True:
        flash("The last name is too short and invalid letters")
        return redirect('/')
    else:
        session["last_name"]=last_name
    if len(email_name)<2 or not EMAIL_REGEX.match(email_name):
        flash("The email is invalid")
        return redirect('/')
    if email_check:
        flash("Email exists already")
        return redirect('/')
    else:
        session["email_name"]=email_name
    if len(password)<7:
        flash("The password is too short")
        return redirect('/')
    if len(confirm_password)<7 or confirm_password!= password:
        flash("The passwords do not match")
        return redirect('/')

    query= "INSERT INTO user_emails (email, first_name, last_name, password, created_at) VALUES (:email, :first_name, :last_name, :password, NOW())"
    data= {
        "email": request.form["email_name"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "password": request.form["password"]
        }
    mysql.query_db(query,data)
    return redirect('/success')

@app.route("/logout", methods=["POST"])
def logsout():
    session.clear()
    return redirect ('/')

app.run(debug=True)
