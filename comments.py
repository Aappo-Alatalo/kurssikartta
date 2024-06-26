from db import db
from sqlalchemy.sql import text


def post_comment(course_id, author_id, rating, comment):
    try:
        sql = "INSERT INTO comments (course_id, author_id, rating, content) VALUES (:course_id, :author_id, :rating, :comment)"
        db.session.execute(
            text(sql),
            {
                "course_id": course_id,
                "author_id": author_id,
                "rating": rating,
                "comment": comment,
            },
        )
        db.session.commit()
    except:
        return False
    return True


def delete_comment(comment_id):
    try:
        sql = "UPDATE comments SET visible=FALSE WHERE id=:comment_id"
        db.session.execute(text(sql), {"comment_id": comment_id})
        db.session.commit()
    except:
        return False
    return True
