from db import db
from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def is_logged_in():
    if session["username"] != None and session["user_id"] != None:
        return True
    else:
        return False


def get_username():
    return session["username"]

def get_user_id():
    return session["user_id"]

def logout():
    del session["user_id"]
    del session["username"]
    del session["account_type"]

def check_username(username):
    sql = "SELECT id, username, password, account_type FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    return result.fetchone()

def login(username, password):
    user = check_username(username) # Check if username is found in the database
    if not user:
        # Invalid username
        return False
    else:
        db_password = user.password
        if check_password_hash(db_password, password):
            # Correct username and password
            session["user_id"] = user.id
            session["username"] = user.username
            session["account_type"] = user.account_type
            return True
        else:
            # Invalid password
            return False
        
def register(username, password):
    if len(username) < 3:
        return False
    if len(password) < 5:
        return False
    
    # Insert data into database
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, account_type) VALUES (:username, :password, 0)"
        db.session.execute(text(sql), {"username":username, "password":password_hash})
        db.session.commit()
    except:
        return False
    
    return login(username, password)