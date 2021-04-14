import os
from flask import Flask, render_template, flash, redirect, session, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField , IntegerField, DateTimeField, DateField, RadioField, SelectField, PasswordField, BooleanField
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
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Appointment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(10), nullable=False)
    middlename = db.Column(db.String(10), nullable=False)
    lastname = db.Column(db.String(10), nullable=False)
    mobile = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    aadhar = db.Column(db.String(10), unique=True, nullable=False)
    dose = db.Column(db.String(10), nullable=False)
    another = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    district = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    timeslot = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Appointment('{self.firstname}', '{self.email}', '{self.aadhar}')"

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

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

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
    flash(f'User Logged out!', 'success')
    return redirect(url_for('home'))

@app.route('/keyThings')
def keyThings():
    return render_template('keyThings.html', title="Key Things")

@app.route('/benefits')
def benefits():
    return render_template('benefits.html', title="Benefits")

@app.route('/info')
def info():
    return render_template('info.html', title="Info")

@app.route('/safety')
def safety():
    return render_template('safety.html', title="Safety")

@app.route('/efficiency')
def efficiency():
    return render_template('efficiency.html', title="Efficiency")

@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    if request.method  == 'POST':
            firstname = request.form.get("firstname")
            middlename = request.form.get("middlename")
            lastname = request.form.get("lastname")
            mobile = request.form.get("mobile")
            email = request.form.get("email")
            address = request.form.get("address")
            dob = request.form.get("dob")
            aadhar = request.form.get("aadhar")
            dose = request.form.get("dose")
            another = request.form.get("another")
            age = request.form.get("age")
            district = request.form.get("district")
            location = request.form.get("location")
            date = request.form.get("date")
            timeslot = request.form.get("timeslot")
            apt= Appointment(firstname=firstname,middlename=middlename,lastname=lastname,mobile=mobile,email=email,
                address=address,dob=dob,aadhar=aadhar,dose=dose,another=another,age=age,
                district=district,location=location,date=date,timeslot=timeslot)
            db.session.add(apt)
            db.session.commit()
            allapt = Appointment.query.all()
            flash(f'{firstname}! Your Appointment is successfully booked!', 'success')
            return redirect(url_for('booking'))
    return render_template('appointment.html', title="Appointment")

@app.route('/booking')
@login_required
def booking():
    allapt = Appointment.query.filter_by(email=current_user.email).all()
    print(allapt)
    return render_template("booking.html", title="Your Booking Details",allapt=allapt, current_user=current_user)
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title=" Error 404"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title= "Error 500"), 500   

if __name__ == '__main__':  
    app.run()