from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash
from db import db, init_db, User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize DB and create tables
init_db(app)

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
            return redirect(url_for('dashboard'))  # Assuming 'dashboard' is the name of the dashboard route
        except Exception as e:
            db.session.rollback()
            flash(f"Error during signup: {str(e)}", 'error')
            logger.error(f"Error during signup: {e}")
            return redirect('/signup')

    return render_template('signup.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    # Render the dashboard page
    return render_template('dashboard.html')  # Replace this with the actual dashboard template or URL

if __name__ == '__main__':
    app.run(debug=True)
