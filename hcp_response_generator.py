import json

class response_generator:

    def __init__(self):
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
                response = response + '<div class="chat-buttons-container"><button><a href="' + json_obj['video_url'] 
                response = response + '" target="_blank">Watch Video</a></button></div>'
            # %% Hyperlink Generation
            print('done3')
            if json_obj['hyperlink_text'] != '' and json_obj['hyperlink_url'] != '':
                if '\n' in json_obj['hyperlink_url']:
                    hyperlinks = json_obj['hyperlink_url'].split('\n')

                    for hyperlink in hyperlinks:
                        response = response + '<a href="' + hyperlink + '" target="_blank">' 
                        response = response + json_obj['hyperlink_text'] + '</a>'
                else:
                    response = response + '<a href="' + json_obj['hyperlink_url'] + '" target="_blank">' 
                    response = response + json_obj['hyperlink_text'] + '</a>'
            # %% Image Generation
            print(json_obj['recommend_intent'],'done4', response)
            # %% Recommend Generation
            if json_obj['recommend_intent'] != '':
                response = response + '<p><b>More information </b></p><a onclick=recommend("' + json_obj['recommend_intent'] + '")>' + json_obj['recommend_intent'] + '</a>'

            print(json_obj['recommend_intent'], 'done4', response)

            if response == '':
                response = "<p>Please try again with different queries</p>"
            
        except Exception as e:
            print('Error')
            response = "<p>Please try again with different queries</p>"
            print(str(e))

        return response