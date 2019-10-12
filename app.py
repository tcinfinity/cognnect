import os
import time
import random
from flask import Flask, session, render_template, flash, redirect, request, make_response, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from forms import SignUpForm, LoginForm

# Every time a record is shown, use updateRecords(username,new)

import face_tilt

specialChars = ['"',"'"]
app = Flask(__name__)

class User():
    username = ""
    password = ""
    pastrecords = ""

def retrievecol(colname, dbname):
    query = 'SELECT ' + colname + ' FROM ' + dbname + ';'
    result = connection.execute(query)
    final = []
    for tup in result:
        temp = tup[0]
        final.append(temp)
    return final

def updateRecords(usern,new):
    global user
    temp = user.pastrecords
    temp += new + ","
    userinfo = retrieverow(usern)[0]
    user.pastrecords = userinfo[3]

def updateUserDB(usern):
    global user
    db.execute("UPDATE cognnectuser SET pastrecords = :pr WHERE username = :un", {"pr": temp, "un": user.username})
    db.commit()

userInfo = []

def retrieverow(username1):
    try:
        result = db.execute("SELECT * FROM cognnectuser WHERE username = :un", {"un": username1}).fetchall()
        return result
    except:
        return None

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

Base = declarative_base()
Base.query = db.query_property()

# Imports user models
def init_db():
    import models
    Base.metadata.create_all(bind=engine)

@app.route('/', methods=['GET','POST'])
def index():
    if 'is_logged' not in session:
        session['is_logged'] = False
    if 'current_user' not in session:
        session['current_user'] = ""
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
        db.execute("INSERT INTO cognnectuser (username, email, password, dorp) VALUES (:un, :em, :pw, :dorp);",{"un": form.username.data, "em": form.email.data, "pw": form.password.data, "dorp": form.dorp.data})
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
    global user
    global userInfo

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
        try:
            userInfo = db.execute("SELECT * FROM cognnectuser WHERE (username = :un);",{"un": form.username.data}).fetchall()
            if len(userInfo) == 0:
                raise Exception('username not found')
        except:
            print('no user exists')
            flash('Login Unsuccessful. Please check your username!', 'danger')
            return redirect(url_for('login', title='Login', form=form))
        ''' userinfo Is A Row Of Data, userinfo[0][3] Is The Password Of User'''

        try:
            if form.password.data == userInfo[0][2]:
                userInfo = retrieverow(form.username.data)[0]
                session['is_logged'] = True
                session['current_user'] = form.username.data

                user = User()

                user.username = userInfo[0]
                user.email = userInfo[1]
                user.password = userInfo[2]
                user.pastrecords = userInfo[3]

                message = 'You have been logged in, ' + session['current_user'] + '!'
                flash(message, 'success')
                return redirect(url_for('myaccount'))
            else:
                print('not matching')
                flash('Login Unsuccessful. Please check username and password and make sure that they are correct!', 'danger')
        except:
            print()
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

@app.route('/tiltpy', methods=['GET', 'POST'])
def tiltpy():
    data = request.json
    data = data['img']

    angle = face_tilt.faceline(face_tilt.from_base64(data))

    response = jsonify(res=angle)
    return response

@app.route('/stroop', methods=['POST', 'GET'])
def stroop():
    return render_template('stroop.html')

@app.route('/stroop_results', methods=['POST'])
def stroop_results():
    data = request.get_json()
    print(data)
    return jsonify(success_user=session['current_user'])

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404
