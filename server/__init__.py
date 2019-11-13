import os
from flask import Flask, abort, session, request, redirect
from flask.json import jsonify
import sqlite3 as sql
import random
import string

app = Flask(__name__, template_folder="../public", static_folder="../public", static_url_path='')

from server.routes import *
from server.services import *

initServices(app)

if 'FLASK_LIVE_RELOAD' in os.environ and os.environ['FLASK_LIVE_RELOAD'] == 'true':
	import livereload
	app.debug = True
	server = livereload.Server(app.wsgi_app)
	server.serve(port=os.environ['port'], host=os.environ['host'])

def generateToken(len):
    password_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(password_characters) for i in range(len))

if not os.path.isfile('database.db'):
    with sql.connect("database.db") as con:  
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS responders(Id integer PRIMARY KEY, Token text, Username text, Password text)')
        cur.execute('CREATE TABLE IF NOT EXISTS patients (qr_token TEXT PRIMARY KEY, priority_tag Text, tag_description Text, first_name Text, last_name Text, age Int, rr Int, pulse Int, capillary_refill Int, bp Text, init_observation Text, locations Text)')
        cur.execute('INSERT INTO responders (Token, Username, Password) VALUES (?, ?, ?)',(generateToken(32),"t@t.com","Password9"))
        con.commit()
       

