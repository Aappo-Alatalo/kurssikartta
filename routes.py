from app import app
from flask import redirect, render_template, request, flash
from os import getenv
import courses
import accounts
import comments

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
        resp = accounts.register(username, password1)
        if resp == True:
            return redirect("/")
        else:
            return render_template("register.html", message=resp)

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
    content = courses.fetch_details(course_id)
    comments = courses.fetch_comments(course_id)
    return render_template("course_template.html", content=content, comments=comments, course_id=course_id)

@app.route("/comment/<course_id>",methods=["GET", "POST"])
def comment(course_id):
    if request.method == "POST": # Send get requests back to course page
        if accounts.is_logged_in(): # Check user is logged in to comment
            comment_text = request.form["new_comment"]
            if comment_text == "":
                flash("Kommentti ei voi olla tyhjä", "error")
                return redirect(f"/courses/{course_id}")
                # TODO: Tämän lisäksi client side check 
            elif len(comment_text) > 500:
                flash("Kommentti on liian pitkä", "error")
                return redirect(f"/courses/{course_id}")

            author = accounts.get_user_id()
            if comments.post_comment(course_id, author, comment_text):
                flash("Kommentti lisätty!", "success")
                return redirect(f"/courses/{course_id}")
            else:
                flash("Komenttin lisäyksessä ilmeni virhe", "error")
                return redirect(f"/courses/{course_id}")
        else:
            flash("Kirjaudu sisään kommentoidaksesi!", "error")
            return redirect(f"/courses/{course_id}")
    else:
        return redirect(f"/courses/{course_id}")