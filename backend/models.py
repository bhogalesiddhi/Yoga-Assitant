from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True,unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(120), nullable=False)

# class Blog(db.Model):
#     __tablename__="blogs"
#     id = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(100),nullable=Flase)
#     content = db