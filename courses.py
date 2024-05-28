from db import db
from sqlalchemy.sql import text

def fetch_details(course_id):
    sql = "SELECT id, name, credits, description, visible FROM courses WHERE courses.id=:course_id"
    result = db.session.execute(text(sql), {"course_id":course_id}).fetchone()
    return result

def fetch_comments(course_id):
    sql = "SELECT users.username, comments.id, comments.content, comments.post_date, visible FROM comments JOIN users ON comments.author_id = users.id WHERE comments.course_id=:course_id"
    result = db.session.execute(text(sql), {"course_id":course_id}).fetchall()
    return result

def fetch_all_courses():
    sql = "SELECT id, name, credits, description, visible FROM courses"
    return db.session.execute(text(sql)).fetchall()

def search_courses(query):
    sql = "SELECT id, name, credits, description, visible FROM courses WHERE name ILIKE :query"
    result = db.session.execute(text(sql), {"query":"%"+query+"%"})
    return result.fetchall()