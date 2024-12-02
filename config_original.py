import os
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv

# Load environment variables from .env file (if you're using one)
load_dotenv()

# Print to debug the variables (you can remove these after confirming they are set correctly)
print("MAIL_USERNAME:", os.getenv('MAIL_USERNAME'))
print("MAIL_PASSWORD:", os.getenv('MAIL_PASSWORD'))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')


app = Flask(__name__)
app.config.from_object(Config)  # Apply config from the Config class

# Access environment variables for email credentials
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Example SMTP server (Gmail)
app.config['MAIL_PORT'] = 587  # TLS port
app.config['MAIL_USE_TLS'] = True  # Use TLS
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Retrieve from environment variable
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Retrieve from environment variable
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Default sender

# Initialize Flask-Mail
mail = Mail(app)

if __name__ == '__main__':
    app.run(debug=True)
