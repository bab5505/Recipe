from models import Recipe
from database import db

def get_all_recipes():
    return Recipe.query.all()

def get_recipe_by_id(recipe_id):
    return Recipe.query.get(recipe_id)

def add_recipe(title, description, instructions, preparation_time, servings):
    recipe = Recipe(title=title, description=description, instructions=instructions,
                    preparation_time=preparation_time, servings=servings)
    db.session.add(recipe)
    db.session.commit()

def delete_recipe(recipe):
    db.session.delete(recipe)
    db.session.commit()
