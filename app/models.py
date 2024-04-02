from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    alternate_email = db.Column(db.String(120), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.relationship('ProfilePicture', backref='user', uselist=False)

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    invitee = db.relationship('User', backref='invitations')

class ProfilePicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    picture_url = db.Column(db.String(255), nullable=False)
