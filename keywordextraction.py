# -*- coding: utf-8 -*-
"""Copy of Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KnAckPaPPTbnZ24E0hh1zVzTO-jrraa9
"""

import nltk
#from nltk import word_tokenize
import string
import re
import pickle
import pandas as pd
#from google.colab import files

new_str=''
arr=[]
def ngrams(tokens, n):
    if n == 0:
        return arr
    if len(tokens) < n - 1:
        return ngrams(tokens, n-1)
    else:
        for j in range(n-1):
            new_str = ''*(n-1-j)
            if j == 0:
                new_str += tokens[j]
            else:
                for i in reversed(range(n-1)):
                    if j-i >=0:
                        new_str += ' '+tokens[j-i]
            arr.append(new_str)
        for i in range(len(tokens)):
            new_str = ''
            for j in range(n):
                if j < n:
                    if (i + j) < len(tokens):
                        if j == 0:
                            new_str += tokens[i+j]
                        else:
                            new_str += ' '+tokens[i+j]
                    else:
                        new_str += ''
            arr.append(new_str)
    return ngrams(tokens, n-1)

#nltk.download('punkt')
stopword_file = open("./data/long_stopwords.txt", "r")
lots_of_stopwords = []



import json
with open("./data/HCP_Intent.json") as json_data:
    intents = json.load(json_data)

for line in stopword_file.readlines():
    lots_of_stopwords.append(str(line.strip()))

stopwords_plus = []
words = []
all_words = []
classes = []
documents = {}
stopwords = []
stopwords_plus = stopwords + lots_of_stopwords
stopwords_plus = set(stopwords_plus)
allWords = []
#sentence = "There are 2 general types of PD symptoms—motor symptoms, which most people are well aware of, and the nonmotor symptoms, which may be unexpected. The nonmotor symptoms of PD, include hallucinations. Currently, there is no clear understanding of the exact cause of hallucinations and delusions associated with PD. However, certain brain chemicals and receptors (such as dopamine and serotonin) are believed to play."
#print('intents',intents)
documents = pd.DataFrame(columns = [ 'Intents', 'Keywords' ])

for intent in intents['data']:
    respo = str(intent['responses'][0])
    
    arr=[]
    new_str=''
    
    for pattern in intent['patterns']:
        
        words = []
        pattern = re.sub(r'[?|$|.|_|(|)|,|&|!]',r'',pattern)
        w = pattern.split(' ')
        w = [(_w.lower()) for _w in w if _w.lower() not in stopwords_plus]
        
        text = ngrams(w, 3)
        text = sorted(list(set(text)))
        words.extend(text)
        words = sorted(list(set(words)))
        
        all_words.append(words)
        
        # print('\n\nwords', words)
        
        # if respo == 'About SAPS-PD':
        #     print('w', w)
        #     print('text', text)
        #     print('response', respo, words)
        
        for word in words:
            if word != '':
                doc = {'Intents': respo.replace("â€™", "'").strip(), 'Keywords': word.strip()}
                docavl = documents.loc[(documents['Intents'] == respo.replace("â€™", "'").strip())
                                       & (documents['Keywords'] == word.strip())]
                # print('docavl', doc)
                if docavl.empty:
                    documents = documents.append(doc, ignore_index = True)


# for intent in intents['data']:
#     for pattern in intent['patterns']:
        
#         pattern = re.sub(r'[?|$|.|_|(|)|,|&|!]',r'',pattern)
#         w = pattern.split(' ')
#         #word = re.sub(r'[?|$|.|_|(|)|,|!]',r'',word)
#         #print("pattern",w)
#         #w = pattern.lower().split(' ')
#         w = [(_w.lower()) for _w in w if _w.lower() not in stopwords_plus]
#         # print("before",w)
#         text = ngrams(w, 3, [])
#         text = sorted(list(set(text)))
#         #print("text",text)
#         words.extend(text)
#         words = sorted(list(set(words)))
    
#     respo = str(intent['responses'][0])
#     # print('intent[', words)
#     allWords.append(words)
#     for word in words:
#         if word != '':
#             doc = {'Intents': respo.replace("â€™", "'").strip(), 'Keywords': word.strip()}
#             docavl = documents.loc[(documents['Intents'] == respo.replace("â€™", "'").strip())
#                                    & (documents['Keywords'] == word.strip())]
#             # print('docavl', doc)
#             if docavl.empty:
#                 documents = documents.append(doc, ignore_index = True)

#     if intent['responses'] not in classes:
#         for response in intent['responses']:
#             resp = response.replace("â€™", "'")
#             classes.append(resp) 
      
#     #words = sorted(list(set(words)))
#     #documents = sorted(list(set(documents)))

# print(documents)

words = sorted(list(set(words)))
with open('./pickles/Consumer_Intent.pkl', 'wb') as f:
  pickle.dump(documents, f)

with open('./pickles/Consumer_ExtractedKeyword.pkl', 'wb') as f:
  pickle.dump(all_words, f)
  #files.download('Consumer_ExtractedKeyword.pkl')
    
# #classes = sorted(list(set(classes)))
# # print(documents)
# #print(classes)




# #for grams in my_ngrams:
#   #print(grams)

