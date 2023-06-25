from flask import Flask, request, render_template, redirect, url_for, session, g, flash
from routes import auth_bp, recipe_bp
from config import Config
from forms import UserAddForm, LoginForm, RecipeForm
from database import db, migrate
from models import User, Recipe
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests

CURR_USER_KEY = 'User_id'

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://robert:cookers5@localhost/recipe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from database import db, migrate

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(recipe_bp)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)

    return app

@app.route('/')
def index():
    app_id = '8840b05c'
    app_key = 'd9dfcdab7d11138e533e7af51fc3a31b'
    query = ''  # Replace with the desired recipe query

    # Make a GET request to the API
    url = f'https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}'
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Extract relevant information from the response
        hits = data['hits']
        recipes = []
        for hit in hits:
            recipe = hit['recipe']

            # Extract the necessary information from the 'recipe' object
            recipe_label = recipe.get('label')
            recipe_url = recipe.get('url')

            recipes.append({
                'name': recipe_label,
                'label': recipe_label,
                'url': recipe_url
            })

        return render_template('index.html', recipes=recipes)
    else:
        return 'Error occurred while fetching recipe data'


@app.before_request
def add_user_to_g():
    """If we're logged in, add current user to Flask global."""
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.get(user_id)
    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session['user_id'] = user.id

@login_manager.user_loader
def load_user(user_id):
    print("Loading user:", user_id)
    return User.query.get(int(user_id))

def do_logout():
    """Logout user."""
    session.pop('user_id', None)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """User signup"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken. Please choose a different username.", 'danger')
        elif form.password.data != form.confirm_password.data:
            flash("Password and confirm password do not match.", 'danger')
        else:
            try:
                user = User.signup(
                    username=form.username.data,
                    password=form.password.data,
                    email=form.email.data,
                    confirm_password=form.confirm_password.data,
                    image_url=form.image_url.data or User.image_url.default.arg
                )

                db.session.add(user)
                db.session.commit()

                # Log in the user after successful signup
                login_user(user)

                # Redirect to the index page
                return redirect(url_for('index'))

            except SQLAlchemyError as e:
                db.session.rollback()
                flash("An error occurred while creating the user: " + str(e), 'danger')

    return render_template('users/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create an instance of the login form
    form = LoginForm()

    # Handle form submission
    if form.validate_on_submit():
        # Retrieve the submitted username and password
        username = form.username.data
        password = form.password.data

        # Authenticate the user
        user = User.authenticate(username, password)

        if user:
            # User authentication successful
            login_user(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(url_for('index'))
        else:
            # Invalid credentials
            flash("Invalid credentials.", "danger")

    # Render the login template with the form
    return render_template('users/login.html', form=form)


@app.route('/users/<int:user_id>')
@login_required
def user_profile(user_id):
    # Get the user data based on the user_id
    user = User.query.get(user_id)

    # Render the user profile template with the user data
    return render_template('users/user.html', user=user)


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    """User logout"""
    logout_user()
    flash("You have successfully logged out.", 'success')
    return redirect(url_for('index'))

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()

    # Handle form submission
    if form.validate_on_submit():
        # Process the form data and add the recipe to the database
        # ...

        flash('Recipe added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_recipe.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
