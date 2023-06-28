from database import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
# from sqlalchemy import Column, Integer

bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(200), default="/static/images/default-pic.png")
    active = db.Column(db.Boolean, default=True)  # Add an active flag to determine if the user account is active

    @classmethod
    def signup(cls, username, email, password, confirm_password, image_url):
        """Sign up user"""
        if password != confirm_password:
            raise ValueError("Password and confirm password do not match")

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`"""
        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        return None

    @property
    def is_active(self):
        # Determine if the user account is active
        return self.active

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='recipes')


# class Recipe(db.Model):
#     __tablename__ = 'recipes'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(100))
#     description = Column(String(500))
#     preparation_time = Column(Integer)  # New column definition
#     servings = Column(Integer)
#     ingredients = Column(String(1000))
#     instructions = Column(String(2000))