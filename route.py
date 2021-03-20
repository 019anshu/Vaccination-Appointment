import os
from flask import Flask, render_template, flash, redirect, session, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField , DateField, RadioField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

app = Flask(__name__)   

app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')

bootstrap = Bootstrap(app)

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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/keyThings')
def keyThings():
    return render_template('keyThings.html')

@app.route('/benefits')
def benefits():
    return render_template('benefits.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/appointment')
def appointment():
    form= ContactUs()
    if request.method == 'POST':
        if form.validate_on_submit:
            name = form.name.data

            flash("Your query is successfully posted!")
            return redirect(url_for('appointment'))
    return render_template('appointment.html',form=form)

@app.route('/safety')
def safety():
    return render_template('safety.html')

@app.route('/efficiency')
def efficiency():
    return render_template('efficiency.html')

@app.route('/vaccinesToYou')
def vaccinesToYou():
    return render_template('vaccinesToYou.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500   

if __name__ == '__main__':  
    app.run()