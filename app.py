import os
from flask import Flask, session, render_template, flash, redirect, request, make_response, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from forms import SignUpForm, LoginForm

specialChars = ['"',"'"]
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# 32-bit key
app.config["SECRET_KEY"] = b'\x9b\xff\xa7p\xdd=p\x1bE\xc8\xd7Q\xb1\xf8\x90\xda\xa6\x89\xd7\xe1\x84\xc8d\xb0\xc8\x17\xc7\xf4\x95\rZc'

is_logged = False

@app.route('/')
@app.route("/index", methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    global is_logged
    unok = True
    emok = True
    if is_logged:
        return redirect(url_for('index'))
    usernames = db.execute("SELECT username FROM cognnectuser").fetchall()
    emails = db.execute("SELECT email FROM cognnectuser").fetchall()

    form = SignUpForm()
    for username in usernames:
        if form.username.data == username[0]:
            unok = False
    for email in emails:
        if form.email.data == email[0]:
            emok = False3

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
    global is_logged
    global current_user
    loginok = False
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data,form.password.data)
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

                is_logged = True
                current_user = form.username.data
                message = 'You have been logged in, ' + current_user + '!'
                flash(message, 'success')
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password and make sure that they are correct!', 'danger')
        except:
            flash('Login Unsuccessful. Please check username and password and make sure that they are correct!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value' # ??
    return resp
