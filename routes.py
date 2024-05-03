from app import app
from flask import redirect, render_template, request
from os import getenv
import courses
import accounts

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    fetched_courses = courses.fetch_all_courses()
    return render_template("index.html", fetched_courses=fetched_courses)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if accounts.login(username, password):
        return redirect("/")
    else:
        return redirect("/")
        
@app.route("/logout")
def logout():
    accounts.logout()
    return redirect("/")

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", message="Salasanat eroavat, yritä uudelleen")
        if accounts.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", message="Rekisteröinti ei onnistunut")

@app.route("/result")
def result():
    query = request.args["query"]
    fetched_courses = courses.search_courses(query)
    return render_template("index.html", fetched_courses=fetched_courses)

@app.route("/courses/") # No course takes user to this route
def courses_page():
    return redirect("/")

@app.route("/courses/<course_id>") # Course details live here
def course_page(course_id):
    return render_template("course_template.html", course=course_id)