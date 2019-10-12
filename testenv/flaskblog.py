import os
from flask import Flask, session, render_template, flash, redirect, request, make_response, url_for, jsonify
from sqlalchemy import create_engine, Table, MetaData
engine = create_engine(os.getenv("DATABASE_URL"))
connection = engine.connect()
app = Flask(__name__)
metadata = MetaData()

cognnectun = Table('cognnectuser', metadata, autoload=True, autoload_with=engine)
print(repr(cognnectun))
print(cognnectun.name)
print(engine.table_names())
egCommand = 'SELECT * FROM cognnectuser'
result = connection.execute(egCommand)
results = result.fetchall()
print("Cognnect Usernames: ", results)
app.secret_key = 'super secret key'

@app.route('/', methods=['GET','POST'])
def index():
    if 'is_logged' not in session:
        session['is_logged'] = False
    return render_template('base.html')
