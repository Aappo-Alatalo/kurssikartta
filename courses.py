from db import db
from sqlalchemy.sql import text

def fetch_average_rating(course_id):
    sql = "SELECT AVG(rating) FROM comments WHERE visible=TRUE AND course_id=:course_id"
    result = db.session.execute(text(sql), {"course_id":course_id}).fetchone()
    return result

def fetch_details(course_id):
    sql = "SELECT id, name, credits, description, visible FROM courses WHERE courses.id=:course_id"
    result = db.session.execute(text(sql), {"course_id":course_id}).fetchone()
    return result

def fetch_comments(course_id):
    sql = "SELECT users.username, comments.id, comments.rating, comments.content, comments.post_date, visible FROM comments JOIN users ON comments.author_id = users.id WHERE comments.course_id=:course_id"
    result = db.session.execute(text(sql), {"course_id":course_id}).fetchall()
    return result

def search_courses(query):
    sql = """
    SELECT 
        A.id, 
        A.name, 
        A.credits, 
        A.description, 
        A.visible, 
        AVG(B.rating) AS average_rating
    FROM 
        courses A
    LEFT JOIN 
        comments B ON A.id = B.course_id AND B.visible = TRUE
    WHERE
        A.name ILIKE :query
    GROUP BY 
        A.id, 
        A.name, 
        A.credits, 
        A.description, 
        A.visible;
    """
    result = db.session.execute(text(sql), {"query":"%"+query+"%"}).fetchall()
    return result