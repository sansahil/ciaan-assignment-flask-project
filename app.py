import os
import logging
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cofounder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Change this
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Change this

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    linkedin = db.Column(db.String(255))
    profile = db.relationship('Profile', backref='user', uselist=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text)
    skills = db.Column(db.String(500))
    location = db.Column(db.String(100))
    age = db.Column(db.Integer)

# Forms
class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    linkedin = StringField('LinkedIn Profile', validators=[Length(max=255)])
    submit = SubmitField('Sign Up')

class SigninForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])

class InviteForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Invite to connect')

# Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            password=hashed_password,
            linkedin=form.linkedin.data
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User signed up successfully!', 'success')
            logger.info(f"User {new_user.username} signed up successfully.")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error during signup: {str(e)}", 'error')
            logger.error(f"Error during signup: {e}")
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.username.data) | (User.email == form.username.data)).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash("Logged in successfully!", "success")
            logger.info(f"User {user.username} logged in successfully.")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password!", "danger")
            logger.error(f"Login attempt failed for {form.username.data}.")
    return render_template('signin.html', form=form)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = serializer.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request',
                          sender='noreply@yourdomain.com',
                          recipients=[user.email])
            msg.body = f'To reset your password, visit the following link: {reset_url}'
            mail.send(msg)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('Email not found.', 'error')
        return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('signin'))
        else:
            flash('User not found.', 'error')
            return redirect(url_for('forgot_password'))
    return render_template('reset_password.html', form=form)

@app.route('/forgot_username', methods=['GET', 'POST'])
def forgot_username():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            msg = Message('Username Recovery',
                          sender='noreply@yourdomain.com',
                          recipients=[email])
            msg.body = f'Your username is: {user.username}'
            mail.send(msg)
            flash("Your username has been sent to your email.", "info")
        else:
            flash("Email not found.", "error")
        return redirect(url_for('signin'))
    return render_template('forgot_username.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('signin'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)

@app.route('/profile/<int:profile_id>', methods=['GET', 'POST'])
def profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    form = InviteForm()
    if form.validate_on_submit():
        # Here you would typically save the invitation to the database
        # and perhaps send an email notification
        flash("Invitation sent successfully!", "success")
        return redirect(url_for('index'))
    return render_template('profile.html', profile=profile, form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

