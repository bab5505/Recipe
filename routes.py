from flask import Blueprint, render_template, redirect, url_for, g, flash
from forms import RecipeForm
from models import Recipe
from database import db
from sqlalchemy.exc import IntegrityError

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes')
def recipe_list():
    if g.user is None:
        return "Please log in to view recipes."

    recipes = Recipe.query.filter_by(user_id=g.user.id).all()
    return render_template('recipe_list.html', recipes=recipes)

@recipe_bp.route('/create', methods=["GET", "POST"])
def recipe_create():
    """Create a new recipe"""
    form = RecipeForm()

    if form.validate_on_submit():
        try:
            # Create a new recipe if the form data passes validation
            recipe = Recipe(
                title=form.title.data,
                description=form.description.data,
                instructions=form.instructions.data,
                ingredients=form.ingredients.data,
                prep_time=form.prep_time.data,
                servings=form.servings.data,
                user_id=g.user.id
            )

            # Store the recipe in the database
            db.session.add(recipe)
            db.session.commit()

            flash("Recipe added successfully.", 'success')

            # Redirect the user to the recipe list
            return redirect(url_for('recipe_bp.recipe_list'))

        except IntegrityError as e:
            flash("An error occurred while adding the recipe.", 'danger')
            return render_template('recipe_create.html', form=form)

    return render_template('recipe_create.html', form=form)

@recipe_bp.route('/<int:recipe_id>', methods=["GET"])
def recipe_detail(recipe_id):
    """Display the details of a specific recipe"""
    recipe = Recipe.query.get(recipe_id)

    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    else:
        flash("Recipe not found.", 'danger')
        return redirect(url_for('recipe_bp.recipe_list'))

@recipe_bp.route('/<int:recipe_id>/edit', methods=["GET", "POST"])
def recipe_edit(recipe_id):
    """Edit an existing recipe"""
    recipe = Recipe.query.get(recipe_id)

    if recipe:
        if recipe.user_id != g.user.id:
            flash("You are not authorized to edit this recipe.", 'danger')
            return redirect(url_for('recipe_bp.recipe_list'))

        form = RecipeForm(obj=recipe)

        if form.validate_on_submit():
            try:
                # Update the recipe with the form data
                recipe.title = form.title.data
                recipe.description = form.description.data
                recipe.instructions = form.instructions.data
                recipe.ingredients = form.ingredients.data
                recipe.prep_time = form.prep_time.data
                recipe.servings = form.servings.data

                # Commit the changes to the database
                db.session.commit()

                flash("Recipe updated successfully.", 'success')

                # Redirect the user to the recipe detail page
                return redirect(url_for('recipe_bp.recipe_detail', recipe_id=recipe.id))

            except IntegrityError as e:
                flash("An error occurred while updating the recipe.", 'danger')
                return render_template('recipe_edit.html', form=form, recipe_id=recipe.id)

        return render_template('recipe_edit.html', form=form, recipe_id=recipe.id)
    else:
        flash("Recipe not found.", 'danger')
        return redirect(url_for('recipe_bp.recipe_list'))

@recipe_bp.route('/<int:recipe_id>/delete', methods=["POST"])
def recipe_delete(recipe_id):
    """Delete an existing recipe"""
    recipe = Recipe.query.get(recipe_id)

    if recipe:
        if recipe.user_id != g.user.id:
            flash("You are not authorized to delete this recipe.", 'danger')
            return redirect(url_for('recipe_bp.recipe_list'))

        db.session.delete(recipe)
        db.session.commit()

        flash("Recipe deleted successfully.", 'success')
    else:
        flash("Recipe not found.", 'danger')

    return redirect(url_for('recipe_bp.recipe_list'))
