import json, os, datetime
import uuid
import config

cfg = config.Config()

config_details = cfg.get_app_configs()

chat_msg_time_format = '%H:%M %p'

if not os.path.exists('History'):
    os.makedirs('History')

def check_buffer_time_to_clear(chats, uid):
    if chats != '':
        chat_his = chats["chats"]
        time_his = []
        if len(chat_his) > 0:
            for chat_h in chat_his:
                time_his.append(chat_h["time"])
        
            max_time = max(time_his)
            max_time = datetime.datetime.strptime(max_time, "%d/%m/%y %H:%M:%S")
            # cur_time = datetime.datetime.strptime(datetime.datetime.now(), "%d/%m/%y %H:%M:%S")
            cur_time = datetime.datetime.now()
            diff = (cur_time - max_time).total_seconds() / 60.0
            print(diff)
            
            chat_clear_buffer_min = int(config_details["chat_clear_buffer_min"])

            if chat_clear_buffer_min < diff:
                chats = {"uid": uid, "chats": []}

    return chats

class History:
    def __init__(self):
        pass

    def check_generate_uid(self, uid):
        if uid == '' or uid == 'null':
            uid = str(uuid.uuid4())
        return uid

    def check_update_history(self, uid, cur_user_chat, cur_bot_chat, user_chat_time):
        
        json_data = {
            "uid": uid,
            "chats": []
        }

        try:
            history_path = 'History/' + uid + '.json'

            if os.path.exists(history_path):
                with open(history_path) as outfile:
                    json_data = outfile.read()
                    json_data = json.loads(json_data)

            json_data = check_buffer_time_to_clear(json_data, uid)

            json_data_chats = json_data["chats"]
            cur_json = {
                "message": cur_user_chat,
                "who": "user",
                "time": user_chat_time)
            }
            json_data_chats.append(cur_json)
            cur_json = {
                "message": cur_bot_chat,
                "who": "bot",
                "time": user_chat_time)
            }
            json_data_chats.append(cur_json)

            if not os.path.exists(history_path):
                with open(history_path, 'w') as outfile:  
                    json.dump(json_data, outfile)
            else:
                with open(history_path, 'r+') as outfile:  
                    json.dump(json_data, outfile)
            
        except Exception as e:
            pass
        
        return json_data

    def get_history_alone(self, uid, finder, geneset, user_chat_time):
        history_path = 'History/' + uid + '.json'
        json_data = {
            "uid": uid,
            "chats": []
        }

        try:
            if os.path.exists(history_path):
                with open(history_path) as outfile:
                    json_data = outfile.read()
                    json_data = json.loads(json_data)
        except:
            json_data = {
                "uid": uid,
                "chats": []
            }   
            pass

        json_data = check_buffer_time_to_clear(json_data, uid)

        if len(json_data["chats"]) <= 0:
            res_json = finder.get_welcome_message()

            welcome_response = geneset.generate_response(res_json)

            json_data = {
                "chats": [{
                    "message": welcome_response,
                    "who": "bot",
                    "time": user_chat_time)
                }],
                "uid": uid
            }

        if not os.path.exists(history_path):
            with open(history_path, 'w') as outfile:  
                json.dump(json_data, outfile)
        
        return json_data
            