from db import db
from sqlalchemy.sql import text

def fetch_all_courses():
    sql = "SELECT name, credits, description FROM Courses"
    return db.session.execute(text(sql)).fetchall()

def search_courses(query):
    sql = "SELECT id, name, credits, description FROM courses WHERE name LIKE :query"
    result = db.session.execute(text(sql), {"query":"%"+query+"%"})
    return result.fetchall()