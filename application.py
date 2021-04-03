import hcp_find_response
import hcp_response_generator
import hcp_get_history
from lazywritter import log_writter
from flask import Flask,request,flash, jsonify
from flask_restful import Resource, Api, reqparse
import subprocess
import time, datetime
import os, sys
import config
import base64
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

logger = log_writter()

geneset = hcp_response_generator.response_generator()

finder = hcp_find_response.response_finder()

@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        return "Unauthorized."
    except Exception as e:
        return str(e)
    

@application.route('/welcome', methods=['GET', 'POST'])
def welcome(): 
    res_json = finder.get_welcome_message()

    response = geneset.generate_response(res_json)

    return response

@application.route('/pred', methods=['GET', 'POST'])
def pred(): 
    user_chat = request.args['conv']
    try:
        import predict

        preds = predict.predict(user_chat)

        response = {"intents" : preds}
    except Exception as e:
        response = {"intents" : str(e)}

    return response

@application.route('/hcpchat', methods=['GET', 'POST'])
def hcpchatbot():
    try:
        history = hcp_get_history.History()
        user_chat = request.args['conv']
        uid = request.args['uid']
        
        res_json = finder.find_HCP_response(user_chat)

        cur_response = geneset.generate_response(res_json)

        uid = history.check_generate_uid(uid)

        history.check_update_history(uid, user_chat, cur_response)

        response = {
            "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}],
            "uid": uid,
            "res_json": res_json
        }
    except Exception as ee:
        response = {
            "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}],
            "uid": "Unknown"
        }

    return response

@application.route('/hcpchathistory', methods=['GET', 'POST'])
def hcpchathistory():
    history = hcp_get_history.History()
    uid = request.args['uid']

    uid = history.check_generate_uid(uid)
    response = history.get_history_alone(uid, finder, geneset)

    return response

@application.route('/patientchat', methods=['GET', 'POST'])
def patientchatbot():
    input = request.args['value']
    return input


@application.route('/refreshCorpus', methods=['GET', 'POST'])
def refreshCorpus():
    import upload_excel_to_database

    corpus_filename='Corpus/Corpus.xlsx'
    corpus_sheetname='Patient_Website_Data'
    upload_excel_to_database.UpdateDB(corpus_filename, corpus_sheetname)
    corpus_sheetname='HCP_Website_Data'
    upload_excel_to_database.UpdateDB(corpus_filename, corpus_sheetname)
    return "Successfully Updated."

# if __name__ == "__main__":
#     application.run(debug=True)
