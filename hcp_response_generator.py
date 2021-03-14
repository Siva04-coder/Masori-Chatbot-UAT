import json

class response_generator:

    def __init__(self):
        pass

    def generate_response(self, json_data):
        response = ''

        try:
            json_obj = json.loads(json_data)

            # %% Plain Text Generation
            if '\n' in json_obj['output_text']:
                txts = json_obj['output_text'].split('\n')

                for txt in txts:
                    response = response + '<p>' + txt + '</p>'
            else:
                response = response + '<p>' + json_obj['output_text'] + '</p>'
            
            # %% Bullet Generation
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
            if json_obj['video_url'] != '':
                response = response + '<div class="chat-buttons-container"><button><a href="' + json_obj['video_url'] 
                response = response + '" target="_blank">Watch Video</a></button></div>'

            # %% Hyperlink Generation
            if json_obj['hyperlink_text'] != '' and json_obj['hyperlink_url'] != '':
                response = response + '<a href="' + json_obj['hyperlink_url'] + '" target="_blank">' 
                response = response + json_obj['hyperlink_text'] + '</a>'

            # %% Image Generation
            # Pending

            if response == '':
                response = "<p>Please try again with different queries</p>"
            
        except Exception as e:
            response = "<p>Please try again with different queries</p>"
            print(str(e))

        return response