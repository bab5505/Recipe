import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://robert:cookers5@localhost/recipe')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_ID = '8840b05c'
    APP_KEY = 'd9dfcdab7d11138e533e7af51fc3a31b'
