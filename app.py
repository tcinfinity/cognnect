import os

from flask import Flask, session, render_template, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from forms import SignUpForm

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# 32-bit key
app.config["SECRET_KEY"] = b'\x9b\xff\xa7p\xdd=p\x1bE\xc8\xd7Q\xb1\xf8\x90\xda\xa6\x89\xd7\xe1\x84\xc8d\xb0\xc8\x17\xc7\xf4\x95\rZc'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('signup.html', form=form)
        else:
            # TODO: check with database for repeats
            return redirect('index.html', signup_success=True)
            # TODO: email confirmation?

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value' # ??
    return resp