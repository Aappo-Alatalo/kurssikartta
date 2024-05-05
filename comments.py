from db import db
from sqlalchemy.sql import text

def post_comment(course_id, author_id, comment):
    try:
        sql = "INSERT INTO comments (course_id, author_id, content) VALUES (:course_id, :author_id, :comment)"
        db.session.execute(text(sql), {"course_id":course_id, "author_id":author_id, "comment":comment})
        db.session.commit()
    except:
        return False

    return True


    