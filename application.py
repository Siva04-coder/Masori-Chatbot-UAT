# %% Import(s)
import hcp_find_response
import hcp_response_generator
import hcp_get_history
import consumer_find_response
import consumer_response_generator
import consumer_get_history
from lazywritter import log_writter
from flask import Flask, request, flash, jsonify
from flask_restful import Resource, Api, reqparse
import subprocess
import time
import datetime
import os
import sys
import config
import base64
from flask_cors import CORS
import auth

# %% Declaration(s) 

application = Flask(__name__)
CORS(application)

logger = log_writter()

geneset = hcp_response_generator.response_generator(logger)

finder = hcp_find_response.response_finder(logger)


consumer_geneset = consumer_response_generator.response_generator(logger)

consumer_finder = consumer_find_response.response_finder(logger)

unauthorized_msg = 'Unauthorized Access.'

chat_msg_time_format = '%d/%m/%y %H:%M:%S'

# %% Common 

@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass
    
    logger.write_activity('Index Logging Activity', 1)
    try:
        return "Welcome."
    except Exception as e:
        return str(e)


@application.route('/welcome', methods=['GET', 'POST'])
def welcome():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass

    res_json = finder.get_welcome_message()

    response = geneset.generate_response(res_json)

    return response


@application.route('/pred', methods=['GET', 'POST'])
def pred():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass

    user_chat = request.headers.get('conv')

    import predict
    
    preds = predict.predict(user_chat)

    response = {"intents": preds}

    return response

# %% HCP 

@application.route('/hcpchat', methods=['GET', 'POST'])
def hcpchatbot():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass

    try:
        history = hcp_get_history.History()
        user_chat = request.headers.get('conv')
        disp_t = request.headers.get('disp_t')
        print('user_chat', disp_t)
        uid = request.args['uid']
        is_recommend = False
        try:
            rec = request.args['rec']
            is_recommend = bool(rec)
        except:
            pass

        res_json = finder.find_response(user_chat, is_recommend)

        cur_response = geneset.generate_response(res_json)

        uid = history.check_generate_uid(uid)

        history.check_update_history(uid, user_chat, cur_response, disp_t)

        if disp_t == 'null':
            disp_t = "raised null"

        response = {
            "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t}],
            "uid": uid
        }
    except Exception as ee:
        logger.write_exception(str(ee), 'hcpchatbot')
        response = {
            "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime(chat_msg_time_format), "display_time": ""}],
            "uid": "Unknown"
        }

    return response

@application.route('/updatefeedback', methods=['GET', 'POST'])
def updatefeedback():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass

    try:
        history = hcp_get_history.History()
        user_chat = request.headers.get('conv')
        disp_t = request.headers.get('disp_t')
        print('user_chat', user_chat)
        uid = request.args['uid']
        is_recommend = False
        try:
            rec = request.args['rec']
            is_recommend = bool(rec)
        except:
            pass

        cur_response = geneset.generate_feedback_response()

        uid = history.check_generate_uid(uid)

        history.check_update_history(uid, user_chat, cur_response, disp_t)

        response = {
            "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t}],
            "uid": uid
        }
    except Exception as ee:
        logger.write_exception(str(ee), 'hcpchatbot')
        response = {
            "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime(chat_msg_time_format), "display_time": ""}],
            "uid": "Unknown"
        }

    return response



@application.route('/hcprecommendchat', methods=['GET', 'POST'])
def hcprecommendchat():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass

    try:
        history = hcp_get_history.History()
        user_chat = request.headers.get('conv')
        disp_t = request.headers.get('disp_t')
        uid = request.args['uid']

        res_json = finder.find_response(user_chat, True)
        cur_response = geneset.generate_response(res_json)
        uid = history.check_generate_uid(uid)

        history.check_update_history(uid, user_chat, cur_response, disp_t)

        response = {
            "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format), "display_time": disp_t}],
            "uid": uid
        }
    except Exception as ee:
        logger.write_exception(str(ee), 'hcpchatbot')
        response = {
            "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime(chat_msg_time_format), "display_time": ""}],
            "uid": "Unknown"
        }

    return response


@application.route('/hcpchathistory', methods=['GET', 'POST'])
def hcpchathistory():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass
    
    disp_t = request.headers.get('disp_t')
    
    history = hcp_get_history.History()
    uid = request.args['uid']

    uid = history.check_generate_uid(uid)
    response = history.get_history_alone(uid, finder, geneset, disp_t)
    
    return response


# %% Consumer

@application.route('/consumerchat', methods=['GET', 'POST'])
def consumerchatbot():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass

    try:
        history = consumer_get_history.History()
        user_chat = request.headers.get('conv')
        uid = request.args['uid']
        is_recommend = False
        try:
            rec = request.args['rec']
            is_recommend = bool(rec)
        except:
            pass

        res_json = consumer_finder.find_response(user_chat, is_recommend)

        cur_response = consumer_geneset.generate_response(res_json)

        uid = history.check_generate_consumer_uid(uid)

        history.check_update_history(uid, user_chat, cur_response)

        response = {
            "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format)}],
            "uid": uid
        }
    except Exception as ee:
        logger.write_exception(str(ee), 'consumerchatbot')
        response = {
            "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime(chat_msg_time_format)}],
            "uid": "Unknown"
        }

    return response


@application.route('/consumerrecommendchat', methods=['GET', 'POST'])
def consumerrecommendchat():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass

    try:
        history = consumer_get_history.History()
        user_chat = request.headers.get('conv')
        uid = request.args['uid']

        res_json = finder.find_response(user_chat, True)
        cur_response = geneset.generate_response(res_json)
        uid = history.check_generate_consumer_uid(uid)

        history.check_update_history(uid, user_chat, cur_response)

        response = {
            "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime(chat_msg_time_format)}],
            "uid": uid
        }
    except Exception as ee:
        logger.write_exception(str(ee), 'consumerrecommendchat')
        response = {
            "chats": [{"message": str(ee), "who": "bot", "time":  datetime.datetime.now().strftime(chat_msg_time_format)}],
            "uid": "Unknown"
        }

    return response


@application.route('/consumerchathistory', methods=['GET', 'POST'])
def consumerchathistory():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return unauthorized_msg
    except Exception as d:
        return unauthorized_msg
        pass

    history = consumer_get_history.History()
    uid = request.args['uid']

    uid = history.check_generate_consumer_uid(uid)
    response = history.get_history_alone(uid, finder, geneset)

    return response

# %% Refresh Corpus to Database

@application.route('/refreshCorpus', methods=['GET', 'POST'])
def refreshCorpus():
    import upload_excel_to_database

    corpus_filename = 'Corpus/Corpus.xlsx'
    corpus_sheetname = 'Patient_Website_Data'
    upload_excel_to_database.UpdateDB(corpus_filename, corpus_sheetname)
    corpus_sheetname = 'HCP_Website_Data'
    upload_excel_to_database.UpdateDB(corpus_filename, corpus_sheetname)
    return "Successfully Updated."

# %% Refresh Pickle Models

@application.route('/refreshHCPModel', methods=['GET', 'POST'])
def refreshHCPModel():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return "Unauthorized Access."
    except Exception as d:
        pass

    import keywordextraction

    return "Model has been updated."

@application.route('/refreshConsumerModel', methods=['GET', 'POST'])
def refreshConsumerModel():
    try:
        auth_creds = request.authorization
        is_authorize = auth.Authorize(
            auth_creds.username, auth_creds.password)
        if is_authorize == False:
            return "Unauthorized Access."
    except Exception as d:
        pass

    import consumer_keywordextraction

    return "Model has been updated."

# %% Main but it should be commented before upload to Git
# if __name__ == "__main__":
#     application.run(debug=True)
