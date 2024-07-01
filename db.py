from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1) # This for Fly.io
db = SQLAlchemy(app)
