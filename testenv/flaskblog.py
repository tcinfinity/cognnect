import os
from flask import Flask, session, render_template, flash, redirect, request, make_response, url_for, jsonify
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
DATABASE_URL="postgres://vzihzhagmfngky:e520bab65138c9d74fc92b5f48330f530dd8a3e33ecb51c9ca2781ea5fd8ddd4@ec2-174-129-226-232.compute-1.amazonaws.com:5432/d6tj5q6d0li4u6"

engine = create_engine(os.getenv("DATABASE_URL"))
connection = engine.connect()
app = Flask(__name__)
metadata = MetaData()
db = scoped_session(sessionmaker(bind=engine))

res = db.execute("SELECT * FROM stroop WHERE (username = 'Admin1')").fetchall()
print(res)
