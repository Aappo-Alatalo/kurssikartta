from db import db
from sqlalchemy.sql import text

def create_suggestion(title, op, description, user_id):
    try:
        sql = """
        INSERT INTO suggestions (name, credits, description, user_id)
        VALUES (:title, :op, :description, :user_id)
        """
        db.session.execute(text(sql), {"title":title, "op":op, "description":description, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False
    
def fetch_suggestions():
    try:
        sql = """
        SELECT A.id, A.name, A.credits, A.description, A.created_at, A.status, B.username
        FROM suggestions A JOIN users B ON
            A.user_id = B.id
        WHERE
            A.status = 'pending'
        ORDER BY
            A.created_at DESC
        """
        res = db.session.execute(text(sql)).fetchall()
        return res
    except:
        return False
    
def remove_suggestion(suggestion_id):
    try:
        sql = "UPDATE suggestions SET status='denied' WHERE id=:suggestion_id"
        db.session.execute(text(sql), {"suggestion_id":suggestion_id})
        db.session.commit()
        return True
    except:
        return False
    
def accept_suggestion(suggestion_id):
    try:
        # Fetch the suggestion data
        sql_fetch = "SELECT name, credits, description FROM suggestions WHERE id=:suggestion_id"
        result = db.session.execute(text(sql_fetch), {"suggestion_id": suggestion_id})
        suggestion = result.fetchone()

        if suggestion:
            name, credits, description = suggestion

            # Insert the suggestion data into the courses table
            sql_insert = """
                INSERT INTO courses (name, credits, description, visible)
                VALUES (:name, :credits, :description, :visible)
            """
            db.session.execute(text(sql_insert), {
                "name": name,
                "credits": credits,
                "description": description,
                "visible": True  # New courses are visible by default
            })

            # Update the suggestion status to 'accepted'
            sql_update = "UPDATE suggestions SET status='accepted' WHERE id=:suggestion_id"
            db.session.execute(text(sql_update), {"suggestion_id": suggestion_id})

            # Commit the transaction
            db.session.commit()
            return True
        else:
            return False  # Suggestion not found
        
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return False