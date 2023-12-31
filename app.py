from flask import Flask, request, render_template, redirect, url_for, session, g, flash
from routes import auth_bp, recipe_bp
from config import Config
from forms import UserAddForm, LoginForm, RecipeForm
from database import db, migrate
from models import User, Recipe
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import requests


CURR_USER_KEY = 'user_id'

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://robert:cookers5@localhost/recipe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
db.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def add_user_to_g():
    """If we're logged in, add the current user to Flask global."""
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.get(user_id)
    else:
        g.user = None


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(recipe_bp)


@app.route('/')
def index():
    # Replace this with your logic to retrieve the list of recipes
    # Example: recipes = Recipe.query.all()
    recipes = [
        {
            'id': 1,
            'title': 'Recipe List',
            # 'description': 'Description 1'
        },
    ]

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
        api_recipes = []
        for hit in hits:
            recipe = hit['recipe']

            # Extract the necessary information from the 'recipe' object
            recipe_name = recipe.get('label')
            recipe_url = recipe.get('url')

            api_recipes.append({
                'name': recipe_name,
                'url': recipe_url
            })

        recipes.extend(api_recipes)

        return render_template('index.html', recipes=recipes)
    else:
        return 'Error occurred while fetching recipe data'


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
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            login_user(user)  # Log in the user
            flash(f"Hello, {user.username}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials.", "danger")

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


@app.route('/recipe')
def recipe():
    # Retrieve the list of recipes from your data source
    recipes = Recipe.query.all()

    print("Number of recipes:", len(recipes))  # Print the number of recipes

    for recipe in recipes:
        print("Recipe title:", recipe.title)  # Print the title of each recipe
        print("Recipe description:", recipe.description)  # Print the description of each recipe

    return render_template('recipe.html', recipes=recipes)


@app.route('/view_recipe/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    # Retrieve the specific recipe from the database using the recipe_id
    recipe = Recipe.query.get(recipe_id)

    if recipe:
        return render_template('recipe_details.html', recipe=recipe)
    else:
        flash("Recipe not found.", "danger")
        return redirect(url_for('recipe'))


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        # Create a new Recipe object and associate it with the current user
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            preparation_time=form.preparation_time.data,
            servings=form.servings.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_recipe.html', form=form)


@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    # Retrieve the specific recipe from the database using the recipe_id
    recipe = Recipe.query.get(recipe_id)

    if recipe:
        print(recipe)
        return render_template('recipe_details.html', recipe=recipe)
    else:
        return 'Recipe not found'

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    # Retrieve the recipe from the database using the recipe_id
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return 'Recipe not found'

    form = RecipeForm(obj=recipe)

    if form.validate_on_submit():
        recipe.title = request.form['title']
        recipe.description = request.form['description']
        recipe.instructions = request.form['instructions']
        recipe.ingredients = request.form['ingredients']
        recipe.preparation_time = int(request.form['preparation_time'])
        recipe.servings = int(request.form['servings'])

        db.session.commit()

        flash("Recipe updated successfully.", "success")
        return redirect(url_for('view_recipe', recipe_id=recipe.id))

    return render_template('edit_recipe.html', form=form, recipe=recipe, recipe_id=recipe_id)


@app.route('/delete_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    # Retrieve the recipe from the database using the recipe_id
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return 'Recipe not found'

    if request.method == 'POST':
        db.session.delete(recipe)
        db.session.commit()

        flash("Recipe deleted successfully.", "success")
        return redirect(url_for('recipe'))

    return render_template('users/delete.html', recipe=recipe)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
