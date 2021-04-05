import os
from flask import Flask, render_template, flash, redirect, session, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField , DateField, RadioField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required, login_manager

app = Flask(__name__)   

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Appointment.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class ContactUs(FlaskForm):
    dose = RadioField('Are you seeking your first of second dose of the COVID-19 vaccine?', choices=[('value1','First Dose'),('value2','Second Dose')], validators=[DataRequired()]) 
    district = SelectField('Check to see which districts are accepting appointments', choices=[('val', '---select---'),('val1', 'Ranchi'), ('val2', 'Gumla'), ('val3', 'Koderma'), ('val4', 'Latehar'), ('val5', 'Garwa'), ('val6', 'Lohardaga'), ('val7', 'Bokaro'), ('val8', 'Dhanbad')], validators=[DataRequired()])
    age = RadioField('Please indicate your age range',choices=[('val1','below age 15'),('val2','between age 16 and 24'),('val3','between age 25 and 34'),('val4','between age 35 and 44'),('val5','between age 45 and 54'),('val6','between age 55 and 64'),('val2','above age 65')], validators=[DataRequired()])
    location = StringField('Appointment Locations', validators=[DataRequired()])
    datetime = DateField('Appointment Date & Time', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    aadhar = StringField('Aadhar', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit' )

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, Please choose another one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, Please choose another one!')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user= User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'{form.username.data}! Your account has been successfully created! You may proceed to Log In', 'success')
            return redirect(url_for('login'))
    return render_template("signup.html", title="Sign Up", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f'{user.username}! You are logged in!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('home'))                
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title="Log In", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/booking')
@login_required
def booking():
    return render_template("booking.html", title="Your Booking Details", current_user=current_user)

@app.route('/keyThings')
def keyThings():
    return render_template('keyThings.html', title="Key Things")

@app.route('/benefits')
def benefits():
    return render_template('benefits.html', title="Benefits")

@app.route('/info')
def info():
    return render_template('info.html', title="Info")

@app.route('/appointment')
@login_required
def appointment():
    form= ContactUs()
    if request.method == 'POST':
        if form.validate_on_submit:
            name = form.name.data

            flash("Your query is successfully posted!")
            return redirect(url_for('appointment'))
    return render_template('appointment.html', title="Appointment",form=form)

@app.route('/safety')
def safety():
    return render_template('safety.html', title="Safety")

@app.route('/efficiency')
def efficiency():
    return render_template('efficiency.html', title="Efficiency")

@app.route('/vaccinesToYou')
def vaccinesToYou():
    return render_template('vaccinesToYou.html', title="Vaccines To You")
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title=" Error 404"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title= "Error 500"), 500   

if __name__ == '__main__':  
    app.run()