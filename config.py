import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/your_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
