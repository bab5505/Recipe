from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hash):
    return check_password_hash(hash, password)

def create_user(username, password, email):
    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password, email=email)
    db.session.add(user)
    db.session.commit()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
