# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_sVmCHsWIzPe3-D6UJbQyemoMWdCcpYC
"""

import nltk
#from nltk import word_tokenize
import string
import re
import pickle
import json

words = []

#nltk.download('punkt')
stopword_file = open("./data/long_stopwords.txt", "r")
lots_of_stopwords = []

for line in stopword_file.readlines():
    lots_of_stopwords.append(str(line.strip()))

stopwords_plus = []
words = []
input = []
intent = []
documents = []
prediction = []
results = []
stopwords = []
arr=[]
stopwords_plus = stopwords + lots_of_stopwords
stopwords_plus = set(stopwords_plus)
inputstr = " "
# st = nltk.PorterStemmer()

try:
    data = pickle.load(open( "./pickles/HCP_ExtractedKeyword.pkl", "rb" ))
    words = data
    intentdata = pickle.load(open( "./pickles/HCP_Intent.pkl", "rb" ))
    # print('intentdata', intentdata)
    intent = intentdata
    # print("intent",intent)
except Exception as e:
    pass

def clean_up_sentence(sentence):
    sentence = re.sub(r'[?|$|.|_|(|)|,|&|!]',r'',sentence)
    w = nltk.word_tokenize(sentence)
    w = [(_w.lower()) for _w in w if _w.lower() not in stopwords_plus]
    
    return w

def bow(sentence, words, show_details=False):
    #sentence_words = clean_up_sentence(sentence)
    # bag of words
    documents = []
    for s in sentence:
        for i,w in enumerate(words):
            #print('words array', w)
            for word in w:
                # if st.stem(word) == st.stem(s):
                if word == s:
                    documents.append(word)
                    #print("Words",documents)
                    if show_details:
                        print ("found in bag: %s" % w)

    
    return(documents)

def predict_bag(intent, output, show_details=False):
    print('output', output)
    for ind in intent.index:
        for wrd in intent['Keywords'][ind].split(' '):
            #print('match', wrd, output)
            for i,w in enumerate(output):
                # print('Stemmer: ', st.stem(w.strip()), st.stem(wrd.strip()))
                # if st.stem(w.strip()) == st.stem(wrd.strip()):
                if w.strip() == wrd.strip():
                    # print(p.stem(w.strip()), p.stem(wrd.strip()), intent['Intents'][ind].replace("â€™", "'"), w, intent['Keywords'][ind].split(' '))
                    if intent['Intents'][ind].replace("â€™", "'") not in prediction:
                        prediction.append(intent['Intents'][ind].replace("â€™", "'"))

    # for s in intent:
    #     print('intent : ', s, ' = ', intent[s])
    #     if s != '':
    #         for i,si in enumerate(s):
    #             #print('output = ', si)
    #             #print("sentence",si.strip())      
    #             for i,w in enumerate(output):  
    #                 if w.strip() == si.strip():
    #                     print(w.strip(), si.strip())
    #                     prediction.append(intent[s].replace("â€™", "'"))
    #                     break
    #                     # print("Words",s[1])
    #                     # if show_details:
    #                     #     print ("found in bag: %s" % w)
            

    return(prediction)


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

def ngrams_custom(tokens):
    ngram_token = []
    temp_token = []
    new_str = ''
    n = len(tokens)
    for j in range(n):
        if tokens[j] != '':
            ngram_token.append(tokens[j])
            if j+1 <= n-1:
                temp_token.append(tokens[j] + " " + tokens[j+1])
    
    for temp in temp_token:
        ngram_token.append(temp)

    return ngram_token


def predict(chat):
    input = []
    inputstr = ""
    processed_list = clean_up_sentence(chat)
    print('processed_list', processed_list)
    inputstr=' '.join(map(str, processed_list))
    input.append(inputstr)
    
    arr=[]
    new_str=''
    #text = ngrams(processed_list, 3)
    text = ngrams_custom(processed_list)
    print('ngram out ', text)
    output = bow(text,words)
    output = sorted(list(set(output)))
    sorted_list = list(sorted(output, key = len, reverse=True))
    print('sorted_list ', sorted_list)
    results= predict_bag(intent,sorted_list)

    return results

#predict("What is OLE ?")

def getGeneralResponse(chat_msg):
    with open("./data/General_Intent.json") as json_data:
        intents = json.load(json_data)

    chat_msg = re.sub(r'[?|$|.|_|(|)|,|&|!]',r'',chat_msg)
    response = ''

    for intent in intents["intents"]:
        tag = intent["tag"]
        patterns = intent["patterns"]
        responses = intent["responses"]
        is_break = False
        for pattern in patterns:
            if str(pattern).lower().strip() == str(chat_msg).lower().strip():
                response = responses[0]
                is_break = True
                break

        if is_break == True:
            break

    print('General response', response)
    
    return response