import json

class response_generator:

    def __init__(self):
        pass

    def generate_response(self, json_data):
        response = ''

        try:
            json_obj = json.loads(json_data)
            if json_obj['display_type'] == 'Welcome':
                if '\n' in json_obj['output_text']:
                    txts = json_obj['output_text'].split('\n')

                    for txt in txts:
                        response = response + '<p>' + txt + '</p>'
                else:
                    response = response + '<p>' + json_obj['output_text'] + '</p>'

            if json_obj['display_type'] == 'Text_with_Bullets':
                if json_obj['output_text'] != '':
                    response = "<p>" + json_obj['output_text'] + "</p>"
                if json_obj['bullet'] != '':
                    response = response + '<ul class="hyperlink">'

                    if '\n' in json_obj['bullet']:
                        bullets = json_obj['bullet'].split('\n')

                        for bull in bullets:
                            response = response + '<li>' + bull + '</li>'
                    else:
                        response = response + '<li>' + json_obj['bullets'] + '</li>'
                
                if response != '':
                    response = response + '</ul>'

            if response == '':
                response = "<p>Please try again with different queries</p>"
            
        except Exception as e:
            response = "<p>Please try again with different queries</p>"
            print(str(e))

        return response