from app import app
from flask import redirect, render_template, request, flash
from os import getenv
from functools import wraps
from secrets import token_hex
import courses
import accounts
import comments

app.secret_key = getenv("SECRET_KEY")

def moderator(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if accounts.is_logged_in() and accounts.get_account_type() == 1:
            return f(*args, **kwargs)
        else:
            flash("403 Access denied", "error")
            return redirect("/")
    return decorated_func

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/")
def index():
    fetched_courses = courses.fetch_all_courses()

    accounts.session["csrf_token"] = token_hex(16)
    return render_template("index.html", fetched_courses=fetched_courses)

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if accounts.session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF Token error", "error")
            return redirect("/")
        
        username = request.form["username"]
        password = request.form["password"]
        resp = accounts.login(username, password)
        if resp == True:
            return redirect(request.referrer)
        else:
            flash(resp, "error")
            return redirect(request.referrer)
    else:
        return redirect("/")
        
@app.route("/logout",methods=["POST"])
def logout():
    if accounts.session["csrf_token"] != request.form["csrf_token"]:
        flash("CSRF Token error", "error")
        return redirect("/")
    
    accounts.logout()
    return redirect("/")

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "GET":
        accounts.session["csrf_token"] = token_hex(16)
        return render_template("register.html", message="")
    if request.method == "POST":
        if accounts.session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF Token error", "error")
            return redirect("/")

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

@app.route("/courses/<course_id>") # Course details live here
def course_page(course_id):
    content = courses.fetch_details(course_id)
    comments = courses.fetch_comments(course_id)
    if accounts.is_logged_in():
        account_type = accounts.get_account_type()
    else:
        account_type = 0

    accounts.session["csrf_token"] = token_hex(16)
    return render_template("course_template.html", content=content, comments=comments, course_id=course_id, account_type=account_type)

@app.route("/comment/<course_id>",methods=["GET", "POST"])
def comment(course_id):
    if request.method == "POST": # Send get requests back to course page
        if accounts.is_logged_in(): # Check user is logged in to comment
            if accounts.session["csrf_token"] != request.form["csrf_token"]:
                flash("CSRF Token error", "error")
                return redirect(f"/courses/{course_id}")
            
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
    
@app.route("/deletecomment/<course_id>/<comment_id>",methods=["POST"])
@moderator
def deletecomment(course_id, comment_id):
    if accounts.session["csrf_token"] != request.form["csrf_token"]:
        flash("CSRF Token error", "error")
        return redirect(f"/courses/{course_id}")

    success = comments.delete_comment(comment_id)
    if success:
        flash("Kommentti poistettu", "success")
    else:
        flash("Kommentin poistamisessa ilmeni ongelma", "error")
    return redirect(f"/courses/{course_id}")