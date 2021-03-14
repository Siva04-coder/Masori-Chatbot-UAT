import pandas as pd
import mysql.connector
import config, json

cfg = config.Config()

config_details = cfg.get_database_configs()

db_user=config_details['db_user']
db_pass=config_details['db_pass']
db_host=config_details['db_host']
database=config_details['db_name']
db_port= config_details['db_port']

class response_finder:

    cnx = ''
    cursor = ''

    def __init__(self):
        self.cnx = mysql.connector.connect(user=db_user, password=db_pass,
                            host=db_host, port=db_port,
                            database=database)

        self.cursor = self.cnx.cursor()

        pass

    def get_welcome_message(self):
        res_query = "Select * from Master_Default_Messages Where lower(Message_Type)= 'welcome'"
        res_json = {}
        try:
            self.cursor.execute(res_query)
            
            table_rows = self.cursor.fetchall()

            df_response = pd.DataFrame(table_rows)
            
            output_text = str(df_response[2][0])
            
            res_json = {
                "output_text": output_text,
                "bullet": '',
                "video_url": '',
                "hyperlink_text": '',
                "hyperlink_url": '',
                "image_url": '',
                "display_type": 'Welcome'
            }

        except Exception as e:
            print(str(e))

        return json.dumps(res_json)

    def remove_stopwords(self, review_words):
        with open('stopwords.txt') as stopfile:
            stopwords_data = stopfile.read()
            stopwords = stopwords_data.splitlines()
            review_words = review_words.split()

            resultwords  = [word for word in review_words if word.lower() not in stopwords]
            
            return resultwords

    def find_response(self, chat_message):
        query = "Select * from master_intent_entity_mapping where Site_Area='HCP' "
        res_query = "Select * from website_data Where lower(Intents)= '"
        res_json = {}
        try:
            chats = self.remove_stopwords(chat_message)
            
            for chat in chats:
                if(chat != ''):
                    chat.replace("'", "\'")
                    query = query + "and lower(Entities) like '%" + chat.lower() + "%' "
            print(query)
            self.cursor.execute(query)
            
            table_rows = self.cursor.fetchall()

            df = pd.DataFrame(table_rows)
            count = len(df)
            
            intent = str(df[1][0])

            intent = intent.replace("'", "")

            res_query = res_query + intent.lower() + "'"

            self.cursor.execute(res_query)
            
            table_rows = self.cursor.fetchall()

            df_response = pd.DataFrame(table_rows)

            display_type = df_response[6][0]

            output_text = '' if df_response[7][0] == 'nan' else df_response[7][0]
            bullet = '' if df_response[8][0] == 'nan' else df_response[8][0]
            video_url = '' if df_response[9][0] == 'nan' else df_response[9][0]
            hyperlink_text = '' if df_response[10][0] == 'nan' else df_response[10][0]
            hyperlink = '' if df_response[11][0] == 'nan' else df_response[11][0]
            image_url = '' if df_response[12][0] == 'nan' else df_response[12][0]
            
            res_json = {
                "output_text": output_text,
                "bullet": bullet,
                "video_url": video_url,
                "hyperlink_text": hyperlink_text,
                "hyperlink_url": hyperlink,
                "image_url": image_url,
                "display_type": display_type
            }

        except Exception as e:
            print(str(e))
            pass

        return json.dumps(res_json)
