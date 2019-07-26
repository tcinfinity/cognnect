from flask_wtf import  FlaskForm
from wtforms import TextField, SelectField, IntegerField, StringField, SubmitField, BooleanField, PasswordField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, EqualTo, Email, Length, DataRequired

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

specialChars = ['"',"'"]
