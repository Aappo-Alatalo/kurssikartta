from db import db
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def is_logged_in():
    return "user_id" in session

def get_username():
    return session["username"]

def get_user_id():
    return session["user_id"]

def get_account_type():
    try:
        return session["account_type"]
    except:
        return 0

def logout():
    del session["user_id"]
    del session["username"]
    del session["account_type"]
    del session["csrf_token"]

def check_username(username):
    sql = "SELECT id, username, password, account_type FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    return result.fetchone()

def login(username, password):
    user = check_username(username) # Check if username is found in the database
    if not user:
        # Invalid username
        return "Käyttäjätunnusta ei löydy, tarkista kirjoititko sen oikein"
    else:
        db_password = user.password
        if check_password_hash(db_password, password):
            # Correct username and password
            session["user_id"] = user.id
            session["username"] = user.username
            session["account_type"] = user.account_type
            session["csrf_token"] = token_hex(16)
            return True
        else:
            # Invalid password
            return "Salasana ei kelpaa, yritä uudelleen"
        
def register(username, password):
    if len(username) < 1:
        return "Käyttäjätunnuksessa tulee olla vähintään yksi merkki"
    if len(password) < 8:
        return "Salasanan tulee olla vähintään kahdeksan merkkiä"
    
    # Insert data into database
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, account_type) VALUES (:username, :password, 0)"
        db.session.execute(text(sql), {"username":username, "password":password_hash})
        db.session.commit()
    except IntegrityError as e:
        return "Käyttäjänimi on jo olemassa, kokeile toista käyttäjänimeä"
    except Exception as e:
        return "Rekisteröinnissä ilmeni yllättävä ongelma, yritä uudelleen"
    
    return login(username, password)