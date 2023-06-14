from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import InputRequired


class RecipeForm(FlaskForm):
    """Form for creating/editing a recipe"""
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    instructions = TextAreaField('Instructions', validators=[InputRequired()])
    ingredients = TextAreaField('Ingredients', validators=[InputRequired()])
    prep_time = StringField('Prep Time', validators=[InputRequired()])
    servings = StringField('Servings', validators=[InputRequired()])


class UserAddForm(FlaskForm):
    """Form for adding a new user"""
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    image_url = StringField('Image URL')


class LoginForm(FlaskForm):
    """Form for user login"""
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
