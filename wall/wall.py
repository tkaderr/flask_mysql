from flask import Flask, redirect, request, render_template, session, flash
from mysqlconnection import  MySQLConnector
import re

app=Flask(__name__)
app.secret_key=("secret_key")

mysql=MySQLConnector(app,"mydb")
FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
LAST_NAME_REGEX =re.compile(r'^[a-zA-Z]*$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def registration_page():
    return render_template("registration.html")

@app.route('/wall')
def logged():
    query1="SELECT users.first_name as first_name, users.last_name as last_name, messages.message as message, messages.id as messages_id, messages.users_id as message_users_id, DATE_FORMAT(messages.created_at, '%M %d %Y %T' ) as created_at FROM users JOIN messages on users.id=messages.users_id order by created_at desc"
    messages=mysql.query_db(query1)
    query2= "SELECT users.first_name as first_name, users.last_name as last_name, comments.id as comments_id, comments.messages_id as message_id, comments.comment as comments, DATE_FORMAT(comments.created_at, '%M %d %Y %T') as created_at from users join comments on users.id=comments.users_id"
    comments=mysql.query_db(query2)
    return render_template("message.html", all_messages=messages, all_posts=comments)

@app.route('/login', methods=["POST"])
def user_login():
    email_name=str(request.form["email_name"])
    password=str(request.form["password"])
    query1 = "SELECT * FROM users WHERE email=:email LIMIT 1"
    data_email= {
        "email": request.form["email_name"]
        }
    email_check=mysql.query_db(query1,data_email)
    if not email_check:
        flash("Email or password incorrect")
        return redirect('/')
    query2 = "SELECT * FROM users WHERE password=:password and email=:email LIMIT 1"
    data_password= {
        "email": request.form["email_name"],
        "password": request.form["password"]
        }
    password_check=mysql.query_db(query2,data_password)
    if not password_check:
        flash("Password is wrong")
        return redirect('/')
    info=mysql.query_db(query2,data_password)
    for ele in info:
        session["first_name"]=ele["first_name"]
        session["last_name"]=ele["last_name"]
        session["email_name"]=ele["email"]
        session["uid"]=ele["id"]
    return redirect('/wall')

@app.route('/register', methods=["POST"])
def user_register():
    first_name=str(request.form["first_name"])
    last_name=str(request.form["last_name"])
    email_name=str(request.form["email_name"])
    password=str(request.form["password"])
    confirm_password=str(request.form["confirm_password"])
    query = "SELECT email FROM users WHERE email=:email"
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

    query= "INSERT INTO users (email, first_name, last_name, password, created_at) VALUES (:email, :first_name, :last_name, :password, NOW())"
    data= {
        "email": request.form["email_name"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "password": request.form["password"]
        }
    mysql.query_db(query,data)
    query2 = "SELECT * FROM users WHERE password=:password and email=:email LIMIT 1"
    data_password= {
        "email": request.form["email_name"],
        "password": request.form["password"]
        }
    userid=mysql.query_db(query2,data_password)
    for ele in userid:
        session["uid"]=ele["id"]
    return redirect('/wall')


@app.route('/messages', methods=['POST'])
def message_index():
    query= "INSERT INTO messages (message, users_id, created_at, updated_at) VALUES (:message, :users_id, NOW(), NOW())"
    data= {
        "message": request.form["message"],
        "users_id": session["uid"]
        }
    mysql.query_db(query,data)
    return redirect('/wall')

@app.route('/comments', methods=['POST'])
def comment_index():
    query= "INSERT INTO comments (comment, users_id, messages_id, created_at, updated_at) VALUES (:comment, :users_id, :messages_id, NOW(), NOW())"
    data= {
        "comment": request.form["commenttxt"],
        "messages_id": request.form["comment"],
        "users_id": session["uid"]
        }

    mysql.query_db(query,data)
    return redirect('/wall')

@app.route('/delete/<message_id>')
def delete(message_id):
    query1= "DELETE FROM comments where comments.messages_id=:m_id"
    query2= "DELETE FROM messages where messages.id =:m_id"
    data ={
        "m_id": message_id
    }
    mysql.query_db(query1,data)
    mysql.query_db(query2,data)
    return redirect('/wall')

@app.route("/logout", methods=["POST"])
def logsout():
    session.clear()
    return redirect ('/')

app.run(debug=True)
