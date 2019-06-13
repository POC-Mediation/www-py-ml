from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
import inspect
#import sqlite3

import sys
import logging
import data_helper
import numpy as np
import pandas as pd
import tensorflow as tf
from pprint import pprint
from tensorflow.contrib import learn


app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None
#db3 = sqlite3.connect('example.db')

f_input = {
    "dispute_id" : "ABR-00001",
    "service_id" : "1, 2 ou 3",
        # 1 : texte décrivant les faits
        # 2 : liste de phrases décrivant les faits
        # 3 : liste de fait
    "facts": ["Fait n°1", "Fait n°2", "Fait n°3"]
}

f_output = [{
    "chapter_id":"",
    "chapter_label":"",
    "clause_id": "",
    "clause_label": ""
}]

sample_req = {
    "dispute_id" : "1086",
    "service_id" : "1",
    "facts": [
        "Le 5 octobre 2012, vous avez eu un accident de la circulation que vous avez déclaré à l'assureur. Un constat amiable d'accident, avec croquis, a été rédigé et signé uniquement par vous, le conducteur adverse ayant refusé de le signer. L'entreprise Thélem a retenu votre entière responsabilité dans ce sinistre et, en l'absence de garantie « dommages », n'a pu intervenir pour l'indemnisation des dommages subis par votre véhicule.Vous avez contesté cette décision en précisant que : « je ne partage pas l'analyse de votre service qui indique un changement de file alors qu'il s'agit d'une fusion de file et qui de toute façon veut faire prévaloir son point de vue sur la priorité à droite pour m'imputer à tort la responsabilité du sinistre » (courriel du 9 octobre 2013)."
    ]
}

def init() :
    global creds, user, password, url, client, db
    if 'VCAP_SERVICES' in os.environ:
        vcap = json.loads(os.getenv('VCAP_SERVICES'))
        print('Found VCAP_SERVICES')
        if 'cloudantNoSQLDB' in vcap:
            creds = vcap['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
    elif "CLOUDANT_URL" in os.environ:
        client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
    elif os.path.isfile('vcap-local.json'):
        with open('vcap-local.json') as f:
            vcap = json.load(f)
            print('Found local VCAP_SERVICES')
            creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
            #db3_cursor = db3.cursor()

init()

def reinit() :
    client.disconnect()
    init()

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('index.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# * https://4569d683-23ea-4885-9890-23e824527523-bluemix.cloudant.com/mydb/_all_docs
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        my_database = client[db_name]
        STR=[]
        #STR = inspect.getmembers(my_database, predicate=inspect.ismethod)
        #STR = STR + '<br>'
        for elt in my_database["_all_docs"]["rows"] :
            STR.append ([my_database[elt["id"]]['name']])
            #STR = STR+'<br>'+my_database[doc]['name']
        return jsonify(STR)
        #return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])


# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    reinit()
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)




@app.route('/api/predictClauses', methods=['GET'])
def get_facts():
    if client:
        my_database = client[db_name]
        STR=[]
        #STR = inspect.getmembers(my_database, predicate=inspect.ismethod)
        #STR = STR + '<br>'
        for elt in my_database["_all_docs"]["rows"] :
            STR.append ([my_database[elt["id"]]['facts']])
            #STR = STR+'<br>'+my_database[doc]['name']
        return jsonify(STR)
        #return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])


@app.route('/api/predictClauses', methods=['POST'])
def put_facts():
    reinit()
    dispute_id = request.json['dispute_id']
    service_id = request.json['service_id']
    rappel_fait = request.json['facts']
    data = {'service_id':service_id,'dispute_id':dispute_id,'facts':rappel_fait}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)




@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
