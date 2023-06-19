from models import Recipe
from database import db

def get_all_recipes():
    return Recipe.query.all()

def get_recipe_by_id(recipe_id):
    return Recipe.query.get(recipe_id)

def add_recipe(title, description, instructions, ingredients, prep_time, servings, user_id):
    recipe = Recipe(
        title=title,
        description=description,
        instructions=instructions,
        ingredients=ingredients,
        prep_time=prep_time,
        servings=servings,
        user_id=user_id
    )
    db.session.add(recipe)
    db.session.commit()

def delete_recipe(recipe):
    db.session.delete(recipe)
    db.session.commit()
