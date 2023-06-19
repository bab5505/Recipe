from flask import Flask
from config import Config
from database import db
from routes import auth_bp, recipe_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)

    return app
