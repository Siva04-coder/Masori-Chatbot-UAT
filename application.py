import subprocess
import time, datetime
import os, sys
import config
import base64
from lazywritter import log_writter
from flask import Flask,request,flash, jsonify
from flask_restful import Resource, Api, reqparse
import hcp_find_response
import hcp_response_generator
import hcp_get_history
from flask_cors import CORS, cross_origin
import ssl

logger = log_writter()

finder = hcp_find_response.response_finder()
geneset = hcp_response_generator.response_generator()
history = hcp_get_history.History()

try:
    raise NotImplementedError("No error")
except Exception as e:
    logger.write_exception('error message', 'method')

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
#, resources={r"/*": {"origins": "*"}}
#app.config['CORS_ORIGINS'] = ['*']
#app.config['CORS_HEADERS'] = ['Content-Type']


class Acadia_HCP_Model(Resource):
    def post(input):
        return "Hello World!" + input


class Acadia_Patient_Model(Resource):
    def post(self):
        pass

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():    
    res_json = finder.get_welcome_message()

    response = geneset.generate_response(res_json)

    return response

@app.route('/calling/', methods=['GET', 'POST', 'OPTIONS'])
def calling():
    print('welcome')
    input = request.args['value']    
    response = jsonify(message=input)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(response)
    return input

@app.route('/hcpchat', methods=['GET', 'POST'])
def hcpchatbot():
    user_chat = request.args['conv']
    uid = request.args['uid']
    
    res_json = finder.find_response(user_chat)

    cur_response = geneset.generate_response(res_json)

    uid = history.check_generate_uid(uid)

    history.check_update_history(uid, user_chat, cur_response)

    response = {
        "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}],
        "uid": uid
    }

    return response

@app.route('/hcpchathistory', methods=['GET', 'POST'])
def hcpchathistory():
    uid = request.args['uid']

    uid = history.check_generate_uid(uid)
    response = history.get_history_alone(uid, finder, geneset)

    return response

@app.route('/patientchat', methods=['GET', 'POST'])
def patientchatbot():
    input = request.args['value']
    return input


@app.route('/refreshCorpus', methods=['GET', 'POST'])
def refreshCorpus():
    import upload_excel_to_database

    corpus_filename='Corpus/Corpus.xlsx'
    corpus_sheetname='Patient_Website_Data'
    upload_excel_to_database.UpdateDB(corpus_filename, corpus_sheetname)
    corpus_sheetname='HCP_Website_Data'
    upload_excel_to_database.UpdateDB(corpus_filename, corpus_sheetname)
    return "Successfully Updated."

#api.add_resource(Acadia_HCP_Model,'/')

#api.add_resource(Acadia_Patient_Model,'/patientmodel')


if __name__ == "__main__":
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.verify_mode = ssl.CERT_REQUIRED
    # context.load_cert_chain('ec2-3-128-171-30.us-east-2.compute.amazonaws.com.crt', 'ec2-3-128-171-30.us-east-2.compute.amazonaws.com.key')
    # context = ('ec2-3-128-171-30.us-east-2.compute.amazonaws.com.crt', 'ec2-3-128-171-30.us-east-2.compute.amazonaws.com.key')#certificate and key files
    # app.run(debug =True,host ='0.0.0.0',port=443,ssl_context=context)
    app.run(host ='0.0.0.0')
