from flask import Flask, request, render_template, redirect, url_for, session, g, flash
from routes import auth_bp, recipe_bp
from config import Config
from forms import RecipeForm, UserAddForm, LoginForm
from database import db, migrate
from models import Recipe, User
from routes import auth_bp, recipe_bp
from sqlalchemy.exc import IntegrityError
# from flask_migrate import Migrate
import requests

CURR_USER_KEY = 'User_id'

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://robert:cookers5@localhost/recipe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.add(user)
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """User login"""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout', methods=["GET"])
def logout():
    """User logout"""
    do_logout()
    flash("You have successfully logged out.", 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
