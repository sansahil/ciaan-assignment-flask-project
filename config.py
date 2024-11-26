import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')

