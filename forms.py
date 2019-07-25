from flask_wtf import from
from wtforms import TextField, SelectField, IntegerField, StringField, SubmitField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, EqualTo, Email, Length

class SignUpForm(Form):
    username = StringField(u'Username', validators=[
        InputRequired('Please enter a username.'),
        Length(min=4, max=16, message='Username can only be 4-16 characters long')
    ])

    email = StringField(u'Email', validators=[
        InputRequired('Please enter your email.'),
        Email('Please enter a valid email.')
    ])

    password = StringField(u'Password', validators=[
        InputRequired('Please enter a password.'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])

    confirm_password = StringField(u'Confirm Password', validators=[
        InputRequired('Please enter the password again.'),
        EqualTo('password', message='Passwords must match'),
    ])

    #age = IntegerField(u'Age', validators=[InputRequired()])
    
    submit = SubmitField('Sign Up')