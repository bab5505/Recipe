# Import the necessary modules and packages
from database import db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

# Define the User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    def __init__(self, username, password, email, image_url=None):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.email = email
        self.image_url = image_url

    @classmethod
    def signup(cls, username, email, password, image_url=None):
        user = User(username=username, email=email, password=password, image_url=image_url)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user

        return False

# Define the Recipe model
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.String(20), nullable=False)
    servings = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('recipes', lazy=True))

    def __init__(self, title, description, instructions, ingredients, prep_time, servings, user_id):
        self.title = title
        self.description = description
        self.instructions = instructions
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.servings = servings
        self.user_id = user_id
