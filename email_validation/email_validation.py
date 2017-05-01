from flask import Flask, render_template, request, session, redirect, flash
from mysqlconnection import  MySQLConnector
import re

app=Flask(__name__)
app.secret_key ="mysecretkey"
mysql=MySQLConnector(app,"emaildb")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def index():
    return render_template("email_validation.html")

@app.route("/success")
def success():
    query ="SELECT * FROM user_emails"
    emails=mysql.query_db(query)
    return render_template("validated.html", all_emails=emails)

@app.route("/delete", methods=["POST"])
def deleted():
    query="DELETE FROM user_emails WHERE id=:id"
    data ={"id": request.form["delete"]}
    mysql.query_db(query,data)
    return redirect("/success")

@app.route("/friends", methods=["POST"])
def create():
    email_name=request.form["email"]
    if len(email_name)<2 or not EMAIL_REGEX.match(email_name):
        flash("The email is invalid")
        return redirect('/')
    else:
        query= "INSERT INTO user_emails (email, created_at) VALUES (:email, NOW())"
        data= {
            "email": request.form["email"]
            }
        mysql.query_db(query,data)
        return redirect('/success')

app.run(debug=True)
