import os, sys, traceback
import time
import random
from flask import Flask, session, render_template, flash, redirect, request, make_response, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from forms import SignUpForm, LoginForm, ChatSearchForm

# Every time a record is shown, use updateRecords(username,new)

import face_tilt

import uuid, base64

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
        db.execute("INSERT INTO cognnectuser (username, firstname, lastname, email, password, dorp) VALUES (:un,:fn, :ln, :em, :pw, :dorp);",{"un": form.username.data,"fn":form.firstname.data,"ln":form.lastname.data, "em": form.email.data, "pw": form.password.data, "dorp": form.dorp.data})
        db.commit()
        flash(f'Account created for {form.firstname.data} {form.lastname.data}!', 'success')
        session['is_logged'] = True
        session['current_user'] = form.username.data
        session["firstname"] = form.firstname.data
        session["fullname"] = form.firstname.data + " " + form.lastname.data
        session["dorp"] = form.dorp.data
        return redirect(url_for('myaccount'))

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

        # store user preference first even if login not successful
        session.permanent = form.remember.data

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
            print("User Info:", userInfo)
            if form.password.data == userInfo[0][4]:
                session['is_logged'] = True
                session['current_user'] = form.username.data
                session['firstname'] = userInfo[0][1]
                session['fullname'] = userInfo[0][1] + " " + userInfo[0][2]
                session['dorp'] = userInfo[0][5]
                print("User Full Name: " + session['fullname'])

                user = User()

                user.username = userInfo[0][0]
                user.email = userInfo[0][3]
                user.password = userInfo[0][4]

                message = 'You have been logged in, ' + session['firstname'] + '!'
                flash(message, 'success')
                return redirect(url_for('myaccount'))
            else:
                print('not matching')
                flash('Login Unsuccessful. Please check username and password and make sure that they are correct!', 'danger')
        except:
            print(traceback.format_exc())
            flash('Login Unsuccessful. Please check username and password and make sure that they are correct!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    stroopInfo = db.execute("SELECT * FROM stroop WHERE (username = :un);",{"un": session['current_user']}).fetchall()
    tiltInfo = db.execute("SELECT * FROM tilt WHERE (username = :un);",{"un": session['current_user']}).fetchall()
    PL = []
    DL = []
    if session['dorp'] == 'd':
        patientList = db.execute("SELECT * FROM chats WHERE (doctor = :un);",{"un": session['current_user']}).fetchall()
        for p in patientList:
            PL.append(p[0])
    elif session['dorp'] == 'p':
        doctorList = db.execute("SELECT * FROM stroop WHERE (username = :un);",{"un": session['current_user']}).fetchall()
        for d in doctorList:
            DL.append(p[0])
    stroopFinalList = []
    for test in stroopInfo:
        temp = {}
        temp['Time'] = test[1]
        temp['CT'] = test[2]
        temp['IT'] = test[3]
        temp['D'] = test[4]
        stroopFinalList.append(temp)
    tiltFinalList = []
    for test in tiltInfo:
        temp = {}
        temp['Time'] = test[1]
        temp['L'] = test[2]
        temp['R'] = test[3]
        tiltFinalList.append(temp)
    return render_template('myaccount.html', stroop=stroopFinalList, tilt=tiltFinalList, pl=PL, dl=DL)

@app.route('/myaccount/patient/<patient_id>', methods=['GET', 'POST'])
def patientaccount(patient_id):
    if session['dorp'] == 'd':
        stroopInfo = db.execute("SELECT * FROM stroop WHERE (username = :un);",{"un": patient_id}).fetchall()
        tiltInfo = db.execute("SELECT * FROM tilt WHERE (username = :un);",{"un": patient_id}).fetchall()
        PL = []
        DL = []
        doctorList = db.execute("SELECT * FROM stroop WHERE (username = :un);",{"un": patient_id}).fetchall()
        stroopFinalList = []
        for test in stroopInfo:
            temp = {}
            temp['Time'] = test[1]
            temp['CT'] = test[2]
            temp['IT'] = test[3]
            temp['D'] = test[4]
            stroopFinalList.append(temp)
        tiltFinalList = []
        for test in tiltInfo:
            temp = {}
            temp['Time'] = test[1]
            temp['L'] = test[2]
            temp['R'] = test[3]
            tiltFinalList.append(temp)

        return render_template('myaccount.html', stroop=stroopFinalList, tilt=tiltFinalList, pl=PL, dl=DL)
    else:
        abort(404)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'is_logged' not in session:
        session['is_logged'] = False

    if session['is_logged']:
        session['is_logged'] = False
        session['current_user'] = None
        session["firstname"] = None
        session["fullname"] = None
        return render_template('index.html', logout=True)
    else:
        return redirect(url_for('index'))

@app.route('/tilt', methods=['GET', 'POST'])
def tilt():

    # inaccessible by doctors
    if session['dorp'] == 'd':
        flash('Sorry, this page is only accessible to patients.',  'warning')
        return redirect('/')

    return render_template('tilt.html')

# receives frame from video, performs ml on server
@app.route('/tiltpy', methods=['GET', 'POST'])
def tiltpy():
    data = request.json
    data = data['img']

    angle = face_tilt.faceline(face_tilt.from_base64(data))

    response = jsonify(res=angle)
    return response

@app.route('/tilt_results', methods=['POST'])
def tilt_results():
    data = request.get_json()
    db.execute("INSERT INTO tilt (username, leftAngle, rightAngle) VALUES (:un, :la, :ra)", {"un": session['current_user'],"la":data["left"],"ra":data["right"]})
    db.commit()
    print(data)
    return jsonify(success_user=session['current_user'])

@app.route('/stroop', methods=['POST', 'GET'])
def stroop():

    # inaccessible by doctors
    if session['dorp'] == 'd':
        flash('Sorry, this page is only accessible to patients.',  'warning')
        return redirect('/')

    return render_template('stroop.html')

@app.route('/stroop_results', methods=['POST'])
def stroop_results():
    data = request.get_json()
    db.execute("INSERT INTO stroop (username, compatibleTime, incompatibleTime, timeDifference) VALUES (:un, :ct, :it, :td)", {"un": session['current_user'],"ct":data["compatibleTime"],"it":data["incompatibleTime"],"td":data["timeDifference"]})
    db.commit()
    print(data)
    return jsonify(success_user=session['current_user'])

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


# chat
@app.route('/chat', methods=['POST', 'GET'])
def chatsearch():
    form = ChatSearchForm()

    # ensure logged in
    if not session['is_logged']:
        # pre-render to skip latency from accessing db
        # form not rendered - not required to parse in arg
        return render_template('chatsearch.html')

    # inaccessible by doctors
    if session['dorp'] == 'd':
        flash('Sorry, this page is only accessible to patients.',  'warning')
        return redirect(url_for('index'))

    if form.validate_on_submit():

        query = form.query.data

        # search for doctor username
        results = db.execute("SELECT * FROM cognnectuser WHERE dorp = 'd' AND username = :username", {"username": query}).fetchall()

        if len(results) == 0:
            flash('Sorry, we can\'t seem to find this doctor. Make sure you\'ve entered the correct username that the doctor has given you.', 'danger')
            return redirect(url_for('chatsearch'))

        else:

            # check if user has already connected with doctor
            possibleConnections = db.execute(
                "SELECT * FROM chats WHERE patient = :patient AND doctor = :doctor",
                {"patient": session['current_user'], "doctor": query}
            ).fetchall()

            # connection exists already
            if len(possibleConnections) > 0: # can put == 1: should not have repeat
                flash('Sorry, you have already been registered with this doctor.', 'warning')
                return redirect(url_for('chatsearch'))

            # create new connection in table chats

            # init uuid for chat url
            # base64 enc for url + shortening
            base_uuid = uuid.uuid4()
            enc_uuid = base64.urlsafe_b64encode(base_uuid.bytes).decode('utf8').rstrip('=') # remove trailing

            db.execute(
                "INSERT INTO chats (patient, doctor, uuid) VALUES (:p, :d, :uuid)",
                {"p": session['current_user'], "d": query, "uuid": enc_uuid}
            )
            db.commit()

            # 1: firstname, 2: lastname
            flash('You have been successfully connected with Dr. ' + results[0][1] + ' ' + results[0][2], 'success')
            return redirect(url_for('chatsearch'))

    # default render
    return render_template('chatsearch.html', form=form)
