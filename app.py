from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT name, credits, description FROM Courses"
    fetched_courses = db.session.execute(text(sql)).fetchall()
    return render_template("index.html", fetched_courses=fetched_courses)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    input_password = request.form["password"]
    # Check user input
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        # TODO: invalid username
        return redirect("/")
    else:
        db_password = user.password
        if check_password_hash(db_password, input_password):
            # Correct username and password
            session["username"] = username
            return redirect("/")
        else:
            # TODO: invalid password
            return redirect("/")
        
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user",methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    # Check user input
    if len(username) < 3:
        # TODO: Show error message, username too short
        return redirect("/")
    elif len(password) < 5:
        # TODO: Show error message, password too short
        return redirect("/")
    # Insert data into database
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, account_type) VALUES (:username, :password, 0)"
    db.session.execute(text(sql), {"username":username, "password":password_hash})
    db.session.commit()
    session["username"] = username
    return redirect("/")