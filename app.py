import random
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import psycopg2
import os
from config import Config

# Initialize Flask app and Flask-Mail
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
app.config.from_object(Config)
mail = Mail(app)

# Utility function to load SQL queries
def load_query(file_name):
    queries_dir = os.path.join(os.path.dirname(__file__), 'queries')
    file_path = os.path.join(queries_dir, file_name)
    with open(file_path, 'r') as file:
        return file.read()

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='postgres'
    )

@app.route('/')
def home():
    return render_template('index.html')
    
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

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Load the SQL query for creating a user
        query = load_query('create_user.sql')

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(query, (first_name, last_name, email, username, hashed_password, linkedin))
            conn.commit()
            cur.close()
            conn.close()

            flash("Account created successfully!", "success")
            return redirect(url_for('signin'))  # Redirect to sign-in page after successful signup
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('signup'))

    return render_template('signup.html')


# Signin route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Load the SQL query for verifying the user
        query = load_query('verify_user.sql')

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(query, (username,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                user_id, db_username, db_password = user
                # Verify the password hash
                if check_password_hash(db_password, password):
                    flash("Login successful!", "success")
                    return redirect(url_for('dashboard'))  # Change 'dashboard' to your desired route
                else:
                    flash("Invalid username or password", "danger")
            else:
                flash("Invalid username or password", "danger")

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    return render_template('signin.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Password reset request route
@app.route('/request-reset', methods=['GET', 'POST'])
def request_reset():
    if request.method == 'POST':
        email = request.form['email']

        query = load_query('get_user_by_email.sql')
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(query, (email,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                flash('You can now reset your password. Enter a new password below.', 'success')
                return redirect(url_for('reset_password', email=email))  # Redirect to reset password page
            else:
                flash('No user found with that email.', 'danger')

        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')

    return render_template('request_reset.html')


# Reset password route
@app.route('/reset-password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password)

        query = load_query('update_password.sql')
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(query, (hashed_password, email))
            conn.commit()
            cur.close()
            conn.close()

            flash('Password reset successfully. You can now log in.', 'success')
            return redirect(url_for('signin'))  # Redirect to signin page after successful reset

        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')

    return render_template('reset_password.html', email=email)


if __name__ == '__main__':
    app.run(debug=True)
