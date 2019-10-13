from flask_wtf import FlaskForm
from wtforms import TextField, SelectField, IntegerField, StringField, SubmitField, BooleanField, PasswordField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, EqualTo, Email, Length, DataRequired

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('error test'), Length(min=4, max=20)])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    dorp = SelectField('Are You a Patient or a Doctor?', choices=[('d', 'Doctor'),('p', 'Patient')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
