import pandas as pd
import mysql.connector
import json
import load_corpus
import predict

class response_finder:

    cnx = ''
    cursor = ''
    welcome_message = ''
    website_data = ''
    master_intent_entity = ''

    def __init__(self):
        self.welcome_message = load_corpus.get_welcome_message()

        self.website_data, self.master_intent_entity = load_corpus.get_HCP_data()


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

        return json.dumps(res_json)

    def remove_stopwords(self, review_words):
        with open('stopwords.txt') as stopfile:
            stopwords_data = stopfile.read()
            stopwords = stopwords_data.splitlines()
            review_words = review_words.split()

            resultwords  = [word for word in review_words if word.lower() not in stopwords]
            
            return resultwords

    def find_HCP_response(self, chat_message, isRecommend=False):
        res_json = {}
        try:
            chat = ''
            if isRecommend == False:
                intent = predict.predict(chat_message)
                print('\n\nAll intents : ', intent)
                chat = intent[0]
            else:
                chat = chat_message
            # chats = self.remove_stopwords(chat_message)
            # master = self.master_intent_entity
            corpus = self.website_data

            # for chat in chats:
            #     if chat != '':
            #         chat.replace("'", "\'")
            #         master = master.loc[(master['Site_Area'] == 'HCP') & (master['Entities'].str.contains(chat))]

            corpus = corpus.loc[(corpus['Sub Functional Area'].str.lower() == str(chat).lower())]
            
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

                print('recommend')
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
                    

            print('\n\nres_json : ', res_json)

        except Exception as e:
            print(str(e))
            pass

        return json.dumps(res_json)


    def find_Consumer_response(self, chat_message, isRecommend=False):
        res_json = {}
        try:
            chat = ''
            if isRecommend == False:
                intent = predict.predict(chat_message)
                print('\n\nAll intents : ', intent)
                chat = intent[0]
            else:
                chat = chat_message
            # chats = self.remove_stopwords(chat_message)
            # master = self.master_intent_entity
            corpus = self.website_data

            # for chat in chats:
            #     if chat != '':
            #         chat.replace("'", "\'")
            #         master = master.loc[(master['Site_Area'] == 'HCP') & (master['Entities'].str.contains(chat))]

            corpus = corpus.loc[(corpus['Sub Functional Area'].str.lower() == str(chat).lower())]
            
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

                print('recommend')
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
                    

            print('\n\nres_json : ', res_json)

        except Exception as e:
            print(str(e))
            pass

        return json.dumps(res_json)
