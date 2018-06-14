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

from sklearn.feature_extraction.text import TfidfVectorizer

tf = TfidfVectorizer(min_df=2, stop_words="english", ngram_range=(0, 6))

tf.fit_transform(documents)
features = tf.get_feature_names()

d = {}
string = '['
for f in features:
    d[f] = {
        'Human': 0,
        'Team': 0
    }
    for i, doc in enumerate(documents):
        if f in doc:
            d[f][targets[i]] += 1
array = []
for key in d.keys():
    if d[key]['Human'] + d[key]['Team'] >= 3:
        array.append({
            "total": d[key]['Human'] + d[key]['Team'],
            "human": d[key]['Human'],
            "team": d[key]['Team'],
            "word": key
        })


def keyProvider(elem):
    return elem['total']


array = sorted(array, key=keyProvider, reverse=True)
for i in array:
    string = string + str(i) + ','
string += ']'
f = open('ABcompare.json', 'w')
f.write(string)
f.flush()
f.close()
