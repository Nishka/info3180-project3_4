from flask import Flask
from flask import render_template, request, session, g, redirect, url_for, abort, flash
from flask_wtf import Form
from wtforms import TextField, PasswordField, validators
from contextlib import closing
import re, sqlite3, os.path

app = Flask(__name__)		#creates an instance of the flask object

#configuring app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR,"wishlist")
SCHEMASQL = os.path.join(BASE_DIR,"schema.sql")
DEBUG = True
SECRET_KEY = 'de#*v*&el@@o1@!_pm*&^sdf&^%en2374t k)()(#$@#$ey?><'
USERNAME = 'admin'
PASSWORD = 'default'
app.config.from_object(__name__)

class User():
    id = ""
    firstname = ""
    lastname = ""
    email = ""
    password = ""
    
    def __init__(self,firstname,lastname,email, password):
        self.firstname = firstname
        self.lastname=lastname
        self.email=email
        self.password=password
        
    def __repr__(self):
        return "<User %r>" % self.email

from routes import *

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
        

@app.before_request
def before_request():
    g.db = connect_db()
    
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


