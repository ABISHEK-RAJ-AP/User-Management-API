from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

def create_user(name, email, phone, password):
    user = User(name=name, email=email, phone=phone, password_hash=hash_password(password))
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def logout_user(user_id):
  
    pass
