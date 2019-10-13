import os
from flask import Flask, session, render_template, flash, redirect, request, make_response, url_for, jsonify
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
DATABASE_URL = "postgres://vzihzhagmfngky:e520bab65138c9d74fc92b5f48330f530dd8a3e33ecb51c9ca2781ea5fd8ddd4@ec2-174-129-226-232.compute-1.amazonaws.com:5432/d6tj5q6d0li4u6"

engine = create_engine(os.getenv("DATABASE_URL"))
connection = engine.connect()
app = Flask(__name__)
metadata = MetaData()
db = scoped_session(sessionmaker(bind=engine))

from sqlfunc import *

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


cognnectun = Table('cognnectuser', metadata, autoload=True, autoload_with=engine)
tableinfo = repr(cognnectun)
tablename = cognnectun.name
alltables = engine.table_names()

def retrieverow(username1):
    result = db.execute("SELECT * FROM cognnectuser WHERE username = :un", {"un": username1}).fetchall()
    return result

userinfo = retrieverow('A1')[0]


app.secret_key = 'super secret key'


user = User()

user.username = userinfo[0]
user.email = userinfo[1]
user.password = userinfo[2]
user.pastrecords = userinfo[3]

def updateRecords(new):
    global user
    temp = user.pastrecords
    temp += new + ","
    db.execute("UPDATE cognnectuser SET pastrecords = :pr WHERE username = :un", {"pr": temp, "un": user.username})
    db.commit()
    userinfo = retrieverow('A1')[0]
    user.pastrecords = userinfo[3]

@app.route('/', methods=['GET','POST'])
def index():
    if 'is_logged' not in session:
        session['is_logged'] = False
    return render_template('base.html')
