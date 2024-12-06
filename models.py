from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    progresses = db.relationship('Progress', backref='user', lazy=True)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), nullable=False)
    task_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)