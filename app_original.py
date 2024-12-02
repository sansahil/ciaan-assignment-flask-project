from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash
from flask_mail import Message
from sample_flask_project.db_setup import db, init_db, User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

app = Flask(__name__)
app.config.from_object('config.Config')

from werkzeug.security import generate_password_hash

# Initialize DB and create tables
init_db(app)

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        linkedin = request.form['linkedin']

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(first_name=first_name, last_name=last_name, email=email, 
                        username=username, password=hashed_password, linkedin=linkedin)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User signed up successfully!', 'success')
            logger.info(f"User {username} signed up successfully.")
            
            # Redirect to the dashboard page
            return redirect(url_for('dashboard'))  # Ensure 'dashboard' route is defined
        except Exception as e:
            db.session.rollback()
            flash(f"Error during signup: {str(e)}", 'error')
            logger.error(f"Error during signup: {e}")
            return redirect('/signup')

    return render_template('signin.html')


# Signin route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', 'success')
            logger.info(f"User {username} logged in.")
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Invalid username or password', 'danger')
            logger.warning(f"Login attempt failed for username: {username}.")
    
    return render_template('signup.html')



if __name__ == '__main__':
    app.run(debug=True)
