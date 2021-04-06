import pandas as pd
import mysql.connector
import json
import load_corpus

class response_finder:

    cnx = ''
    cursor = ''
    welcome_message = ''
    website_data = ''
    master_intent_entity = ''
    logger = ''

    def __init__(self, _logger):
        self.logger = _logger
        self.welcome_message = load_corpus.get_welcome_message()

        self.website_data, self.master_intent_entity = load_corpus.get_Consumer_data()


    def get_welcome_message(self):
        res_query = "Select * from Master_Default_Messages Where lower(Message_Type)= 'welcome'"
        res_json = {}

        try:            
            res_json = {
                "output_text": self.welcome_message,
                "bullet": '',
                "video_url": '',
                "hyperlink_text": '',
                "hyperlink_url": '',
                "image_url": '',
                "display_type": 'Welcome',
                "recommend_intent": '',
                "visit_page": ''
            }

        except Exception as e:
            print(str(e))
            self.logger.write_exception(str(e), 'get_welcome_message')

        return json.dumps(res_json)

    def remove_stopwords(self, review_words):
        with open('stopwords.txt') as stopfile:
            stopwords_data = stopfile.read()
            stopwords = stopwords_data.splitlines()
            review_words = review_words.split()

            resultwords  = [word for word in review_words if word.lower() not in stopwords]
            
            return resultwords

    def find_response(self, chat_message, isRecommend=False):
        res_json = {}
        try:
            chat = ''
            intent = []
            import consumer_predict
            if isRecommend == False:
                intent = consumer_predict.predict(chat_message)
                print('\n\nAll intents : ', intent)
                if len(intent) > 0:                
                    if isRecommend == True:
                        try:
                            intent.remove(chat_message)
                        except:
                            pass
                    chat = intent[0]
            else:
                chat = chat_message
            # chats = self.remove_stopwords(chat_message)
            # master = self.master_intent_entity
            corpus = self.website_data
            print('\n\nIntent Tried: ', chat, '\n')
            # for chat in chats:
            #     if chat != '':
            #         chat.replace("'", "\'")
            #         master = master.loc[(master['Site_Area'] == 'HCP') & (master['Entities'].str.contains(chat))]
            if chat != '':
                corpus = corpus.loc[(corpus['Sub Functional Area'].str.strip().lower() == str(chat).strip().lower())]
                
                if not corpus.empty:
                    print('\n\ncorpus : ', corpus)
                    print('\n\nintent : ', chat)
                    output_text = '' if str(corpus['Response'].iloc[0]) == 'nan' else corpus['Response'].iloc[0]
                    bullet = '' if str(corpus['Bullets'].iloc[0]) == 'nan' else corpus['Bullets'].iloc[0]
                    video_url = '' if str(corpus['Video URL'].iloc[0]) == 'nan' else corpus['Video URL'].iloc[0]
                    hyperlink_text = '' if str(corpus['Hyperlink Text'].iloc[0]) == 'nan' else corpus['Hyperlink Text'].iloc[0]
                    hyperlink = '' if str(corpus['Hyperlink URL'].iloc[0]) == 'nan' else corpus['Hyperlink URL'].iloc[0]
                    image_url = '' if str(corpus['Image URL'].iloc[0]) == 'nan' else corpus['Image URL'].iloc[0]
                    #recommend_text = '' if str(corpus['Recommend Text'].iloc[0]) == 'nan' else corpus['Recommend Text'].iloc[0]
                    recommend_intent = '' if str(corpus['Recommend Intent'].iloc[0]) == 'nan' else corpus['Recommend Intent'].iloc[0]
                    visit_page = '' if str(corpus['Visit Page'].iloc[0]) == 'nan' else corpus['Visit Page'].iloc[0]

                    res_json = {
                        "output_text": output_text,
                        "bullet": bullet,
                        "video_url": video_url,
                        "hyperlink_text": hyperlink_text,
                        "hyperlink_url": hyperlink,
                        "image_url": image_url,
                        #"recommend_text": recommend_text,
                        "recommend_intent": recommend_intent,
                        "visit_page": visit_page
                    }
                else:
                    cnt = 1
                    while True:
                        try:
                            if len(intent) == 0:
                                break
                            chat = intent[cnt]
                            chat = chat

                            corpus = self.website_data
                            corpus = corpus.loc[corpus['Sub Functional Area'].str.lower() == str(chat).lower()]
                            
                            if not corpus.empty:
                                print('\n\corpus : ', corpus)
                                print('\n\nintent : ', chat)
                                output_text = '' if str(corpus['Response'].iloc[0]) == 'nan' else corpus['Response'].iloc[0]
                                bullet = '' if str(corpus['Bullets'].iloc[0]) == 'nan' else corpus['Bullets'].iloc[0]
                                video_url = '' if str(corpus['Video URL'].iloc[0]) == 'nan' else corpus['Video URL'].iloc[0]
                                hyperlink_text = '' if str(corpus['Hyperlink Text'].iloc[0]) == 'nan' else corpus['Hyperlink Text'].iloc[0]
                                hyperlink = '' if str(corpus['Hyperlink URL'].iloc[0]) == 'nan' else corpus['Hyperlink URL'].iloc[0]
                                image_url = '' if str(corpus['Image URL'].iloc[0]) == 'nan' else corpus['Image URL'].iloc[0]
                                #recommend_text = '' if str(corpus['Recommend Text'].iloc[0]) == 'nan' else corpus['Recommend Text'].iloc[0]
                                recommend_intent = '' if str(corpus['Recommend Intent'].iloc[0]) == 'nan' else corpus['Recommend Intent'].iloc[0]
                                visit_page = '' if str(corpus['Visit Page'].iloc[0]) == 'nan' else corpus['Visit Page'].iloc[0]

                                res_json = {
                                    "output_text": output_text,
                                    "bullet": bullet,
                                    "video_url": video_url,
                                    "hyperlink_text": hyperlink_text,
                                    "hyperlink_url": hyperlink,
                                    "image_url": image_url,
                                    #"recommend_text": recommend_text,
                                    "recommend_intent": recommend_intent,
                                    "visit_page": visit_page
                                }
                                break

                            cnt = cnt + 1
                        except Exception as e:
                            break
                            pass
            
            if not bool(res_json):
                response = consumer_predict.getGeneralResponse(chat_message)
                # print('response', response)
                if str(response).strip() == '':
                    response = "I don't understand your question. Try asking the question in different way or ask me about something else."
                res_json = {
                    "output_text": response,
                    "bullet": '',
                    "video_url": '',
                    "hyperlink_text": '',
                    "hyperlink_url": '',
                    "image_url": '',
                    #"recommend_text": recommend_text,
                    "recommend_intent": '',
                    "visit_page": ''
                }

            print('\n\nres_json : ', res_json)

        except Exception as e:
            print(str(e))
            self.logger.write_exception(str(e), 'find_response')
            pass

        return json.dumps(res_json)

