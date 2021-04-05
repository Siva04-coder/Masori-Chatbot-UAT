import json

class response_generator:

    logger = ''

    def __init__(self, _logger):
        self.logger = _logger
        pass

    def generate_response(self, json_data):
        response = ''

        try:
            print('json_data', json_data)
            json_obj = json.loads(json_data)
            print('json', json_obj)
            # %% Plain Text Generation
            if '\n' in json_obj['output_text']:
                txts = json_obj['output_text'].split('\n')

                for txt in txts:
                    response = response + '<p>' + txt + '</p>'
            else:
                response = response + '<p>' + json_obj['output_text'] + '</p>'
            
            # %% Bullet Generation
            print('done1')
            if json_obj['bullet'] != '':
                response = response + '<ul class="hyperlink">'

                if '\n' in json_obj['bullet']:
                    bullets = json_obj['bullet'].split('\n')

                    for bull in bullets:
                        response = response + '<li>' + bull + '</li>'
                else:
                    response = response + '<li>' + json_obj['bullets'] + '</li>'
            
                if '<ul class="hyperlink">' in response:
                    response = response + '</ul>'
            # %% Video Generation
            print('done2')
            if json_obj['video_url'] != '':
                response = response + '<div class="chat-text-divider"></div>'
                response = response + '<div class="chat-buttons-container"><button><a href="' + json_obj['video_url'] 
                response = response + '" target="_blank">Watch Video</a></button></div>'
            # %% Hyperlink Generation
            print('done3')
            if json_obj['hyperlink_text'] != '' and json_obj['hyperlink_url'] != '':
                response = response + '<div class="chat-text-divider"></div>'
                
                if '\n' in json_obj['hyperlink_url']:
                    hyperlinks = json_obj['hyperlink_url'].split('\n')
                    hyperlink_texts = json_obj['hyperlink_text'].split('\n')
                    cnt = 0
                    for hyperlink in hyperlinks:
                        txt = json_obj['hyperlink_text']
                        try:
                            txt = hyperlink_texts[cnt]
                        except Exception as e:
                            pass
                        
                        response = response + '<p><a href="' + hyperlink + '" target="_blank">' 
                        response = response + txt + '</a></p>'

                        cnt = cnt + 1
                else:
                    response = response + '<a href="' + json_obj['hyperlink_url'] + '" target="_blank">' 
                    response = response + json_obj['hyperlink_text'] + '</a>'
            # %% Image Generation
            print(json_obj['recommend_intent'],'done4', response)
            # %% Recommend Generation
            if json_obj['recommend_intent'] != '':
               response = response + '<div class="chat-text-divider"></div>'
                response = response + '<p><b>Recommend topic for you </b></p>'

                if '\n' in json_obj['recommend_intent']:
                    recommend_intents = json_obj['recommend_intent'].split('\n')
                    
                    for recommend_intent in recommend_intents:
                        response = response + '<a href="#" onclick="recommend(\'' + recommend_intent + '\')">' + recommend_intent + '</a>'
                else:
                    response = response + '<a href="#" onclick="recommend(\'' + json_obj['recommend_intent'] + '\')">' + json_obj['recommend_intent'] + '</a>'

            # %% Visit Page Generation
            if json_obj['visit_page'] != '':
                response = response + '<div class="chat-text-divider"></div>'
                response = response + '<div class="chat-buttons-container"><button style="width: 100%"><a href="' + json_obj['visit_page'] 
                response = response + '" target="_blank">Visit Page</a></button></div>'

            print(json_obj['recommend_intent'], 'done4', response)

            if response == '':
                response = "<p>I don't understand your question. Try asking the question in different way or ask me about something else.</p>"
            
        except Exception as e:
            print('Error')
            response = "<p>I don't understand your question. Try asking the question in different way or ask me about something else.</p>"
            print(str(e))
            self.logger.write_exception(str(e), 'generate_response')

        return response