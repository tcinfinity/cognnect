import os
import time
import random
from flask import Flask, session, render_template, flash, redirect, request, make_response, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from forms import SignUpForm, LoginForm

import face_tilt

specialChars = ['"',"'"]
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# 32-bit key
app.config["SECRET_KEY"] = b'\xd4*Y\xc3/Q\xa68\xd8\xd2\x9da\x9a\x1c\xeaM+\xd0\x12\xd7\xd1\xb7+\xdd'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route('/', methods=['GET','POST'])
def index():
    if 'is_logged' not in session:
        session['is_logged'] = False
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    unok = True
    emok = True
    if 'is_logged' not in session:
        session['is_logged'] = False

    if session['is_logged']:
        return redirect(url_for('index')) #TODO: ,is_logged=True
    usernames = db.execute("SELECT username FROM cognnectuser").fetchall()
    emails = db.execute("SELECT email FROM cognnectuser").fetchall()

    form = SignUpForm()

    # TODO: async load
    for username in usernames:
        if form.username.data == username[0]:
            unok = False
    for email in emails:
        if form.email.data == email[0]:
            emok = False

    '''Check For Duplicate Username & Email'''
    if form.validate_on_submit() and unok and emok:
        print(form.username.data, form.email.data, form.password.data)
        db.execute("INSERT INTO cognnectuser (username, email, password) VALUES (:un, :em, :pw);",{"un": form.username.data, "em": form.email.data, "pw": form.password.data})
        db.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))

    elif not unok and emok:
        flash(f'The username "{form.username.data}" has been taken!', 'danger')
        return render_template('signup.html', form=form)

    elif not emok and unok:
        flash(f'The email "{form.email.data}" has been registered already!', 'danger')
        return render_template('signup.html', form=form)

    elif not unok and not emok:
        flash(f'The username "{form.username.data}" and email "{form.email.data}" have both been taken!', 'danger')
        return render_template('signup.html', form=form)

    '''Return Same Website If Fields Do Not Satisfy Requirements'''
    return render_template('signup.html', form=form)
    
    # TODO: email confirmation?

@app.route("/login", methods=['GET', 'POST'])
def login():
    loginok = False
    form = LoginForm()

    if form.validate_on_submit():
        print(str(form.remember.data))
        print(form.username.data, form.password.data)
        '''
        Check For Special Characters As Part Of Special Characters
        '''
        for letter in form.password.data:
            for character in specialChars:
                if letter == character:
                    flash('Login Unsuccessful. Please check username and password for any special characters!', 'danger')
                    return render_template('login.html', title='Login', form=form)
        try:
            for letter in form.username.data:
                for character in specialChars:
                    if letter == character:
                        flash('Login Unsuccessful. Please check username and password for any special characters!', 'danger')
                        return render_template('login.html', title='Login', form=form)
        except:
            print(form.username.data,specialChars)
        '''
        Check If Username & Password Are Matching Pairs
        '''

        userinfo = db.execute("SELECT * FROM cognnectuser WHERE (username = :un);",{"un": form.username.data}).fetchall()
        ''' userinfo Is A Row Of Data, userinfo[0][3] Is The Password Of User'''

        try:
            if form.password.data == userinfo[0][2]:

                session['is_logged'] = True
                session['current_user'] = form.username.data
                message = 'You have been logged in, ' + session['current_user'] + '!'
                flash(message, 'success')
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password and make sure that they are correct!', 'danger')
        except:
            flash('Login Unsuccessful. Please check username and password and make sure that they are correct!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    return render_template('myaccount.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'is_logged' not in session:
        session['is_logged'] = False

    if session['is_logged']:
        session['is_logged'] = False
        session['current_user'] = None
        return render_template('index.html', logout=True)
    else:
        return redirect(url_for('index'))

@app.route('/tilt', methods=['GET', 'POST'])
def tilt():
    return render_template('tilt.html')

@ app.route('/tiltpy', methods=['GET', 'POST'])
def tiltpy():
    data = request.form.get('img')
    print(request.form)

    angle = face_tilt.faceline(face_tilt.from_base64(data))
    return angle

@app.route("/stroop", methods=['POST'])
def stroop():
    
        tstart = time.time()
        wordList = ["Red", "Blue", "Green", "Yellow"]
        colourList = ["Red", "Blue", "Green", "Yellow"]
        temp1 = random.randint(0,3)
        temp2 = random.randint(0,3)
        answer = input(wordList[temp1] + " " + colourList[temp2])
        notDone = True
        while notDone:
            if answer == wordList[temp1]:
                print(answer)
                tend = time.time()
                print(tend-tstart)
                notDone = False
            else:
                answer = input(wordList[temp1] + " " + colourList[temp2])

# @app.errorhandler(404)
# def not_found(error):
#     resp = make_response(render_template('error.html'), 404)
#     resp.headers['X-Something'] = 'A value' # ??
#     return resp
