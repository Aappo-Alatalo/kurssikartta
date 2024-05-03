from db import db
from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def logout():
    del session["username"]

def check_username(username):
    sql = "SELECT id, username, password FROM users WHERE username=:username"
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
            session["username"] = user.username
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