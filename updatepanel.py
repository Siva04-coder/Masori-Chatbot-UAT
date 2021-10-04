import json
from flask import request

#######################################   UPDATE PANEL #################################################

#######################################    Consumer   ###################################################

def get_dropdown_intent_consumer():   
    b=[]
    with open(r'data/intent.json','r') as f:
        data = json.load(f)
        for x in data['data']:          
            #print(x['responses'])
            b.append(x['responses'])
        return b

def show_dropdownIntent_Keywords_ConSubFunctionalArea():
    if request.method=='POST':
        response=request.form['Intent_consumer']
    with open(r'data/intent.json','r') as f:                        
        data = json.load(f)
        for x in data['data']:
            a=x['patterns']
            b=x['responses']
            for words in b:
                if response==words:
                    return a

def del_keywords_ConSubFunctionalArea():
    if request.method=='POST':
        response=request.form['del_word']
        response1=request.form['Intent_consumer']
        org=response.replace("|","'")

        with open(r'data/intent.json') as f:
            data=json.load(f)
            for  x in data['data']:
                z=x['responses']
                y=x['patterns']
                for words in z:
                    if words==response1:
                        y.remove(org)
                    
        with open(r"data/intent.json", "w") as fw:
            json.dump(data, fw)

        import consumer_keywordextraction

def Show_Keywords_ConAutoSuggestion():   
    with open(r'data/All_Consumer_Keywords.json') as f:
        data2=json.load(f)
        return data2['keywords']

def get_new_Keywords_ConAutoSuggestion():
    if request.method=='POST':
        response=request.form['Keyword']
        
        with open(r'data/All_Consumer_Keywords.json') as f:
            data=json.load(f)
            x=data['keywords']
            x.append(response)

        with open(r"data/All_Consumer_Keywords.json", "w") as fw:
            json.dump(data, fw)

def delete_Keywords_ConAutoSuggestion():
    if request.method=='POST':
        response=request.form['KeywordDelete']
        res=response.replace("|","'")

        with open(r'data/All_Consumer_Keywords.json') as f:
            data=json.load(f)
            x=data['keywords']
            x.remove(res)

        with open(r"data/All_Consumer_Keywords.json", "w") as fw:
            json.dump(data, fw)

def Add_Keyword_ConSubFunctionalArea():
    if request.method=='POST':
        response=request.form['Add_Keyword']
        response1=request.form['Intent_consumer']
        
        with open(r'data/intent.json') as f:
            data=json.load(f)
            for  x in data['data']:
                z=x['responses']
                y=x['patterns']
                for words in z:
                    if words==response1:
                        y.append(response)

        with open(r"data/intent.json", "w") as fw:
            json.dump(data, fw)

        import consumer_keywordextraction
        
#######################################    HCP   ###################################################
def get_dropdown_intent_HCP():  
    w=[] 
    with open(r'data/HCP_intent.json','r') as f:
        data = json.load(f)
        for x in data['data']:          
            #print(x['responses'])
            w.append(x['responses'])
        return w
def show_dropdownIntent_Keywords_HCPSubFunctionalArea():
    if request.method=='POST':
        response=request.form['Intent_hcp']
    with open(r'data/HCP_intent.json','r') as f:                        
        data = json.load(f)
        for x in data['data']:
            a=x['patterns']
            b=x['responses']
            for words in b:
                if response==words:
                    return a 

def Show_Keywords_HCPAutoSuggestion():   
    with open(r'data/All_HCP_Keywords.json') as f:
        data2=json.load(f)
        return data2['keywords']

def get_new_Keywords_HCPAutoSuggestion():
    if request.method=='POST':
        response=request.form['Keyword']
        
        with open(r'data/All_HCP_Keywords.json') as f:
            data=json.load(f)
            x=data['keywords']
            x.append(response)
        
        with open(r"data/All_HCP_Keywords.json", "w") as fw:
            json.dump(data, fw)


def del_keywords_HCPSubFunctionalArea():
    if request.method=='POST':
        response=request.form['del_word']
        response1=request.form['Intent_hcp']
        org=response.replace("|","'")
        
        with open(r'data/HCP_intent.json') as f:
            data=json.load(f)
            for  x in data['data']:
                z=x['responses']
                y=x['patterns']
                for words in z:
                    if words==response1:
                        y.remove(org)

        with open(r"data/HCP_intent.json", "w") as fw:
            json.dump(data, fw)

        import keywordextraction
                

def Add_Keyword_HCPSubFunctionalArea():
    if request.method=='POST':
        response=request.form['Add_Keyword']
        response1=request.form['Intent_hcp']

        with open(r'data/HCP_intent.json') as f:
            data=json.load(f)
            for  x in data['data']:
                z=x['responses']
                y=x['patterns']
                for words in z:
                    if words==response1:
                        y.append(response)

        with open(r"data/HCP_intent.json", "w") as fw:
            json.dump(data, fw)

        import keywordextraction

def delete_Keywords_HCPAutoSuggestion():
    if request.method=='POST':
        response=request.form['KeywordDel']
        org1=response.replace("|","'")
        with open(r'data/All_HCP_Keywords.json') as f:
            data=json.load(f)
            x=data['keywords']
            x.remove(org1)

        with open(r"data/All_HCP_Keywords.json", "w") as fw:
            json.dump(data, fw)
        

