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

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route("/")
def index():
    fetched_courses = courses.search_courses("", "trending")

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
    accounts.session["latest_search"] = query # Save query for smoother UI
    sort = request.args["sort"]
    accounts.session["latest_sort"] = sort # Save sort for smoother UI

    fetched_courses = courses.search_courses(query, sort)
    return render_template("index.html", fetched_courses=fetched_courses)

@app.route("/courses/<course_id>") # Course details live here
def course_page(course_id):
    try: # Fix SQL Data error
        if int(course_id) > 999999999:
            return redirect("/")
    except:
        return redirect("/")
    
    content = courses.fetch_details(course_id)
    average_rating = courses.fetch_average_rating(course_id)[0]
    comments = courses.fetch_comments(course_id)
    enrollments = courses.fetch_enrollments(course_id)
    is_enrolled = "Kirjaudu sisään ilmoittautuaksesi kurssille"
    if accounts.is_logged_in():
        account_type = accounts.get_account_type()
        user_id = accounts.get_user_id()
        is_enrolled = courses.is_enrolled(course_id, user_id)
    else:
        account_type = 0

    accounts.session["csrf_token"] = token_hex(16)
    return render_template("course_template.html",
                            content=content,
                            average_rating=average_rating,
                            comments=comments, course_id=course_id,
                            account_type=account_type,
                            enrollments=enrollments,
                            is_enrolled=is_enrolled
                            )

@app.route("/comment/<course_id>",methods=["GET", "POST"])
def comment(course_id):
    if request.method == "POST": # Send get requests back to course page
        if accounts.is_logged_in(): # Check user is logged in to comment
            if accounts.session["csrf_token"] != request.form["csrf_token"]:
                flash("CSRF Token error", "error")
                return redirect(f"/courses/{course_id}")
            
            comment_text = request.form.get("new_comment")
            if comment_text == "":
                flash("Kommentti ei voi olla tyhjä", "error")
                return redirect(f"/courses/{course_id}")
                # TODO: Tämän lisäksi client side check 
            elif len(comment_text) > 500:
                flash("Kommentti on liian pitkä", "error")
                return redirect(f"/courses/{course_id}")

            rating = request.form["rating"]
            if not rating:
                flash("Muista lisätä arvosteluusi tähdet!", "error")
                return redirect(f"/courses/{course_id}")
            elif rating not in ["1", "2", "3", "4", "5"]:
                flash("Tähtiarvostelussa ilmeni virhe", "error")
                return redirect(f"/courses/{course_id}")
            
            rating = int(rating)
            
            author = accounts.get_user_id()
            if comments.post_comment(course_id, author, rating, comment_text):
                flash("Arvostelu lisätty!", "success")
                return redirect(f"/courses/{course_id}")
            else:
                flash("Arvostelun lisäyksessä ilmeni virhe", "error")
                return redirect(f"/courses/{course_id}")
        else:
            flash("Kirjaudu sisään arvostellaksesi kurssin!", "error")
            return redirect(f"/courses/{course_id}")
    else:
        return redirect(f"/courses/{course_id}")
    
@app.route("/deletecomment/<course_id>/<comment_id>",methods=["POST"])
@moderator
def delete_comment(course_id, comment_id):
    if accounts.session["csrf_token"] != request.form["csrf_token"]:
        flash("CSRF Token error", "error")
        return redirect(f"/courses/{course_id}")

    success = comments.delete_comment(comment_id)
    if success:
        flash("Arvio poistettu", "success")
    else:
        flash("Arvion poistamisessa ilmeni ongelma", "error")
    return redirect(f"/courses/{course_id}")

@app.route("/enroll",methods=["POST"])
def enroll(): 
    course_id = request.form["course_id"]
    if not course_id or not course_id.isnumeric():
        flash("Kurssia ei ole", "error")
        return redirect("/")
    course_id = int(course_id)

    if accounts.is_logged_in():
        if accounts.session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF Token error", "error")
            return redirect(f"/courses/{course_id}")
        
        user_id = accounts.get_user_id()
        response = courses.enroll(course_id, user_id)
        if response == True:
            flash("Ilmoittautuminen onnistui!", "success")
            return redirect(f"/courses/{course_id}")
        else:
            flash(response, "error")
            return redirect(f"courses/{course_id}")

    else:
        flash("Kirjaudu sisään ilmoittatuaksesi kurssille", "error")
        return redirect(f"courses/{course_id}")
        
@app.route("/cancelenrollment",methods=["POST"])
def cancel_enrollment():
    course_id = request.form["course_id"]
    if not course_id or not course_id.isnumeric():
        flash("Kurssia ei ole", "error")
        return redirect("/")
    course_id = int(course_id)

    if accounts.is_logged_in():
        if accounts.session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF Token error", "error")
            return redirect(f"/courses/{course_id}")
        
        user_id = accounts.get_user_id()
        response = courses.cancel_enrollment(course_id, user_id)
        if response == True:
            flash("Ilmoittautumisen peruminen onnistui!", "success")
            return redirect(f"/courses/{course_id}")
        else:
            flash("Ilmoittatumisen peruminen epäonnistui", "error")
            return redirect(f"courses/{course_id}")

    else:
        flash("Kirjaudu sisään peruaksesi kurssi-ilmoittautumisesi", "error")
        return redirect(f"courses/{course_id}")