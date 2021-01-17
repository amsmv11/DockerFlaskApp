#!/usr/bin/env python
# encoding: utf-8

"""
APP RUNS ON PORT 5000
"""
import json
from flask import Flask, request, jsonify, redirect, render_template
import sqlite3
import hashlib

app = Flask(__name__)





@app.route("/users/<string:name>/<string:password>/", methods=['POST'])
def createUser(name, password):
    if name != "" and password != "":
        name = name.replace("<", "")
        name = name.replace(">", "")
        name = name.replace("script", "")
        name = name.replace("=", "")
        name = name.replace(";", "")
        name = name.replace(":", "")

        result = hashlib.md5(password.encode()) 
        res = result.hexdigest()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?,?)", (name, res))
        conn.commit()
        conn.close()
        return redirect("/users/list")
    else:
        return "<h1>ERROR: username and password missing</h1>"


@app.route("/users/list/", methods=['GET'])
def listUsers():
    res = "<h1>List of all users</h1> <br> <ul>"

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    conn.commit()
    query = c.fetchall()
    conn.close()

    if query != []:
        for id, user, password in query:
            user = user.replace("<", "")
            user = user.replace(">", "")
            user = user.replace("script", "")
            user = user.replace("=", "")
            user = user.replace(";", "")
            user = user.replace(":", "")
            res += "<li> Username: " + user + " <br> Password: " + password + "</li>"

    else:
        res += "<li>EMPTY_LIST</li>"

    res += "</ul>"
    return res


@app.route("/redirect/", methods=['GET'])
def redirectTest():
    return redirect("https://www.google.com")

@app.route("/<string:name>/", methods=['GET'])
def helloName(name):
    return "Hi " + name + "! \nDocker is easy"

@app.route("/repeatName/<string:name>/<int:nr>/", methods=['GET', 'POST'])
def helloNameTimesNr(name, nr):
    response = ""
    if request.method == "POST":
        response += "POST METHOD\n"
    else:
        response += request.method + "\n"
    for i in range(nr):
        response += "Hello " + name +"!\n"
    return jsonify({'response':response})

@app.route('/', methods=['GET'])
def query_records():
    # name = request.args.get('name')
    # print(name)
    # with open('./data.txt', 'r') as f:
    #     data = f.read()
    #     records = json.loads(data)
    #     for record in records:
    #         if record['name'] == name:
    #             return jsonify(record)
    #     return jsonify({'error': 'data not found'})
    return "<h1>Flask API<h1><br>"\
            "<ul>"\
                "<li>/name/</li>"\
                "<li>/repeatName/name/nr_of_times/</li>"\
                "<li>/redirect/  (goes to google)</li>"\
                "<li>/users/create/name/password</li>"\
                "<li>/users/list</li>"\
                

@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    with open('./data.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('./data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)

@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open('./data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['name'] == record['name']:
            r['email'] = record['email']
        new_records.append(r)
    with open('./data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)
    
@app.route('/', methods=['DELETE'])
def delte_record():
    record = json.loads(request.data)
    new_records = []
    with open('./data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['name'] == record['name']:
                continue
            new_records.append(r)
    with open('./data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

# app.run(debug=True)
app.run(host="0.0.0.0")