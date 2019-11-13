from server import app
from flask import render_template
import json
import os
import sqlite3 as sql
from flask import jsonify, request

@app.route('/')
def hello_world():
    return "Server is Up and Running!", 200 
    #return app.send_static_file('index.html')

#Newly Added Routes
@app.route("/getT1Patients", methods=['POST'])
def getT1Patients():
    content = request.json
    #Parameters requested from JSON
    if not set(('token', )).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401
        
    return getCategoryPatient("T1")

@app.route("/getT2Patients", methods=['POST'])
def getT2Patients():
    content = request.json
    #Parameters requested from JSON
    if not set(('token', )).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401
        
    return getCategoryPatient("T2")

@app.route("/getT3Patients", methods=['POST'])
def getT3Patients():
    content = request.json
    #Parameters requested from JSON
    if not set(('token', )).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401
        
    return getCategoryPatient("T3")

@app.route("/getT4Patients", methods=['POST'])
def getT4Patients():
    content = request.json
    #Parameters requested from JSON
    if not set(('token', )).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401
        
    return getCategoryPatient("T4")

@app.route("/getPatient", methods=['POST'])
def getPatientData():
    content = request.json
    #Parameters requested from JSON
    if not set(('token','qr_token')).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401

    qr_token = content['qr_token']

    with sql.connect("database.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM patients WHERE qr_token = ?",(qr_token,))
        patient = cur.fetchone()
        
        if patient is None:
            return "Patient not found in database", 400
        else:
            return jsonify(dict(patient))

@app.route("/editPatient", methods=['POST'])
def editPatientData():
    content = request.json
    #Parameters requested from JSON
    if not set(('token','qr_token')).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401
    content.pop('token')
    
    qr_token = content['qr_token']
    
    with sql.connect("database.db") as con:
        cur = con.cursor()
        if 'locations' in content:
            cur.execute('UPDATE patients SET locations = ? WHERE qr_token = ?', (json.dumps(content['locations']),qr_token))
            content.pop('locations')
        try:    
            for (k, v) in content.items():
                cur.execute('UPDATE patients SET "{}" = ? WHERE qr_token = ?'.format(k.replace('"', '""')), (v,qr_token))
        except:
            return "Parameter not in Database", 570  
        con.commit()
        
    return "Patient Edited"


@app.route("/addPatient", methods=['POST'])
def createPatientData():
    content = request.json
    #Parameters requested from JSON
    if not set(('token','qr_token','priority_tag','tag_description','first_name','last_name','age','rr','pulse','capillary_refill','bp','init_observation','locations')).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401

    qr_token = content['qr_token']
    priority_tag = content['priority_tag']
    tag_description = content['tag_description']
    first_name = content['first_name']
    last_name = content['last_name']
    age = int(content['age'])
    rr = int(content['rr'])
    pulse = int(content['pulse'])
    capillary_refill = int(content['capillary_refill'])
    bp = content['bp']
    init_observation = content['init_observation']
    locations = json.dumps(content['locations'])

    with sql.connect("database.db") as con:
        cur = con.cursor()
        try: 
            cur.execute('INSERT INTO patients (qr_token, priority_tag, tag_description, first_name, last_name, age, rr, pulse, capillary_refill, bp, init_observation, locations) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (qr_token,priority_tag,tag_description,first_name,last_name,age,rr,pulse,capillary_refill,bp,init_observation,locations))
            con.commit()
        except:
            return "Duplicate Record", 570  
      
    return "Patient Added to Database", 200

@app.route("/getLocations", methods=['POST'])
def getLocations():
    content = request.json
    #Parameters requested from JSON
    if not set(('token',)).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401

    with sql.connect("database.db") as con:
        cur = con.cursor()
        locT1 = []
        locT2 = []
        locT3 = []
        locT4 = []

        for row in cur.execute("SELECT locations FROM patients WHERE priority_tag = ?",("T1",)):
            for loc in json.loads(row[0]):
                locT1.append(loc['lat'] + "," + loc['long'])
        for row in cur.execute("SELECT locations FROM patients WHERE priority_tag = ?",("T2",)):
            for loc in json.loads(row[0]):
                locT2.append(loc['lat'] + "," + loc['long'])
        for row in cur.execute("SELECT locations FROM patients WHERE priority_tag = ?",("T3",)):
            for loc in json.loads(row[0]):
                locT3.append(loc['lat'] + "," + loc['long'])
        for row in cur.execute("SELECT locations FROM patients WHERE priority_tag = ?",("T4",)):
            for loc in json.loads(row[0]):
                locT4.append(loc['lat'] + "," + loc['long'])

    return jsonify({"t1": locT1,"t2": locT2,"t3": locT3,"t4": locT4})


@app.route("/respondInfo", methods=['POST'])
def respondInfo():
    content = request.json
    #Parameters requested from JSON
    if not set(('token',)).issubset(content): return "Invalid Parameters", 400
    #Check Token Validity
    token = content['token']
    if not validToken(token): return "Invalid User Token", 401

    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT Username FROM responders WHERE Token = ?",(token,))
        user = cur.fetchone()
        
        if user is None:
            return "Responder not found in Database", 400
        else:
            username = user[0]
            return jsonify({"username":username})

@app.route("/login", methods=['POST'])
def loginUser():
    content = request.json
    #Parameters requested from JSON
    if not set(('username','password')).issubset(content): return "Invalid Parameters", 400

    usr = content['username']
    pwd = content['password']

    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT Token FROM responders WHERE Username = ? AND Password = ?",(usr,pwd))
        user1 = cur.fetchone()
        
        if user1 is None:
            return "Responder not found in database", 400
        else:
            token = user1[0]
            return jsonify({"token":token})

def validToken(token):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        for row in cur.execute("SELECT Token FROM responders WHERE Token= ?",(token,)):
            return True
        else:
            return False

def getCategoryPatient(category):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT first_name,last_name,init_observation FROM patients WHERE priority_tag = ?",(category,))
        patients = cur.fetchall()

        if patients is None:
            return "No " + category + " Patients in Database", 400
        else:
            patArray = []
            for row in patients:
                patArray.append({
                    "first_name": row[0],
                    "last_name": row[1],
                    "init_observation": row[2]
                })
            return jsonify(patArray)

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')
