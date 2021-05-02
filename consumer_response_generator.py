import json


class response_generator:

    logger = ''

    def __init__(self, _logger):
        self.logger = _logger
        pass

    def generate_feedback_response(self):
        response = ''

        try:
            # %% Plain Text Generation
            response = response + 'Thank you for your feedback. Everyday I am learning. I will answer your questions to the best of my ability.'
        except Exception as e:
            print('Error')
            response = "<p>I am sorry can you rephrase your question?</p>"
            print(str(e))
            self.logger.write_exception(str(e), 'get_welcome_message')

        return response

    def generate_response(self, json_data):
        response = ''
        try:
            isMoreInfo = False
            print('json_data', json_data)
            json_obj = json.loads(json_data)
            print('json', json_obj)
            # %% Plain Text Generation
            if '\n' in json_obj['output_text']:
                txts = json_obj['output_text'].split('\n')

                for txt in txts:
                    response = response + '<p>' + txt + '</p>'
            else:
                if json_obj['output_text'] != '':
                    response = response + '<p>' + json_obj['output_text'] + '</p>'
                

            # if "I don't understand your question" in json_obj['output_text']:
            #     response = response + '<div class="chat-text-divider"></div>'
            #     response = response + '<a href="https://nuplazid-masori.azurewebsites.net/frequently-asked-questions" target="_blank" >Click here to see FAQ</a>'

            if 'Goodbye' in json_obj['output_text'] or 'My pleasure' in json_obj['output_text']:
                response = response + '<div class="chat-individual-feedback"><span>Was this helpful?</span>'
                response = response + \
                    '<button class="chat-individual-feedback-button-no" onclick="feedbackno()">No</button>'
                response = response + \
                    '<button class="chat-individual-feedback-button-yes" onclick="feedbackyes()">Yes</button>'
                response = response + '<div class="chat-float-clear"></div></div>'

            # %% Bullet Generation
            print('done1')
            if json_obj['bullet'] != '':
                response = response + '<ul>'

                if '\n' in json_obj['bullet']:
                    bullets = json_obj['bullet'].split('\n')

                    for bull in bullets:
                        response = response + '<li>' + bull + '</li>'
                else:
                    response = response + '<li>' + \
                        json_obj['bullets'] + '</li>'

                if '<ul>' in response:
                    response = response + '</ul>'
            # %% Video Generation
            print('done2')
            if json_obj['video_url'] != '':
                response = response + '<div class="chat-text-divider"></div>'
                response = response + \
                    '<div class="chat-buttons-container"><button><a href="' + \
                    json_obj['video_url']
                response = response + '" target="_blank">Watch Video</a></button></div>'
            # %% Hyperlink Generation
            print('done3')
            if json_obj['hyperlink_text'] != '' and json_obj['hyperlink_url'] != '':
                response = response + '<div class="chat-text-divider"></div>'

                if '\n' in json_obj['hyperlink_url']:
                    hyperlinks = json_obj['hyperlink_url'].split('\n')
                    hyperlink_texts = json_obj['hyperlink_text'].split('\n')
                    cnt = 0
                    response = response + '<ul>'
                    for hyperlink in hyperlinks:
                        txt = json_obj['hyperlink_text']
                        try:
                            txt = hyperlink_texts[cnt]
                        except Exception as e:
                            pass

                        response = response + '<li><a href="' + hyperlink + '" target="_blank">'
                        response = response + txt + '</a></li>'

                        cnt = cnt + 1
                    response = response + '</ul>'
                else:
                    response = response + '<a href="' + \
                        json_obj['hyperlink_url'] + '" target="_blank">'
                    response = response + json_obj['hyperlink_text'] + '</a>'
            # %% Image Generation

            # %% Visit Page Generation
            if json_obj['visit_page'] != '':
                response = response + '<div class="chat-text-divider"></div>'
                response = response + '<div class="chat-buttons-container"><div style="float:left;padding-top: 7px;">Here is a link that may help </div>'
                response = response + '<div style="float:right"><button><a href="' + \
                    json_obj['visit_page']
                response = response + '" target="_blank">Click here</a></button></div></div>'
                isMoreInfo = True

            print(json_obj['recommend_intent'], 'done4', response)
            # %% Recommend Generation
            if json_obj['recommend_intent'] != '':
                if isMoreInfo == True:
                    response = response + '<div class="chat-text-divider" style="margin-top: 33px"></div>'
                else:
                    response = response + '<div class="chat-text-divider"></div>'
                response = response + "<p><b>Here's what I found </b></p>"
                response = response + '<ul>'
                if '\n' in json_obj['recommend_intent']:
                    recommend_intents = json_obj['recommend_intent'].split(
                        '\n')

                    for recommend_intent in recommend_intents:
                        if recommend_intent.strip() != '':
                            response = response + \
                                '<li><a href="#" class="recommended" onclick="recommend(this)">' + \
                                recommend_intent + '</a></li>'
                else:
                    response = response + \
                        '<li><a href="#" class="recommended" onclick="recommend(this)">' + \
                        json_obj['recommend_intent'] + '</a></li>'
                response = response + '</ul>'

            print(json_obj['recommend_intent'], 'done4', response)

            if response == '':
                response = "<p>I am sorry can you rephrase your question?</p>"
                response = response + '<div class="chat-text-divider"></div>'
                response = response + '<a href="https://nuplazid-masori.azurewebsites.net/frequently-asked-questions" target="_blank">Click here to see FAQ</a>'
            else:
                response = response + '<div id="lookingfeedback"><div class="chat-text-divider"></div>'
                response = response + '<p>Is there anything else you are looking for?</p>'
                response = response + '<button class="chat-feedback-button-no" onclick="feedbacklookingno()">No</button>'
                response = response + '<button class="chat-feedback-button-yes" onclick="feedbacklookingyes()">Yes</button></div>'

        except Exception as e:
            print('Error')
            response = "<p>I am sorry can you rephrase your question?</p>"
            print(str(e))
            self.logger.write_exception(str(e), 'get_welcome_message')

        return response

    def feedback_generator(feedback):
        response = ''
        try:
            if feedback == "Yes":
                response = response + '<p>How may I help you?</p>'
            else:
                response = response + "<p>Thank you! I'm so glad I could help.</p>"
        except:
            pass

        return response