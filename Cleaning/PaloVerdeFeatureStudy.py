import os
import pandas as pd

path = './Palo'

textFiles = os.listdir(path)
textToRead = pd.read_csv('./palo.csv')

dictionary = {}
d = {}
for index, item in textToRead.iterrows():
    dictionary[str(item[0])] = str(item[3])

new_dict = {}
documents = []
targets = []
for file in os.listdir(path):
    check = file.split('R')[0]
    if check in dictionary.keys():
        documents.append(open(path + '/' + file, 'r').read().strip().replace("\n", " ").lower())
        targets.append(dictionary[check])

area_of_interest = ['burden response', 'condition prohibited technical', 'abnormal', 'ability operate',
                    'alarm response procedure', 'briefing', 'capable performing', 'cause', 'technical specification',
                    'cognitive', 'decision making', 'dec process', 'bus']
from nltk.tokenize import word_tokenize, sent_tokenize

f = open('text.txt', 'a')
for i, doc in enumerate(documents):

    sentences = sent_tokenize(doc)
    for sentence in sentences:
        for area in area_of_interest:

            if area in sentence:
                f.write(sentence + '\n\n' + area + ":" + targets[i] + '\n\n')

f.flush()
f.close()

"""
Interesting KeyWords : cognitive, cause, decision making
"""
