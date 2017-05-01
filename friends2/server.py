from flask import Flask, render_template, request, session, redirectflash
from mysqlconnection import  MySQLConnector

app=Flask(__name__)

app.secret_key ="mysecretkey"

mysql=MySQLConnector(app,"friends2db")

@app.route("/")
def index():
    query ="SELECT * FROM friends2"
    friends=mysql.query_db(query)
    return render_template("index.html", all_friends=friends)

@app.route("/friends", methods=["POST"])
def create():
    query= "INSERT INTO friends2 (full_name, age, created_at) VALUES (:full_name, :age, NOW())"
    data= {
        "full_name": request.form["full_name"],
        'age':  request.form['age'],
        }
    mysql.query_db(query,data)
    return redirect('/')

app.run(debug=True)
