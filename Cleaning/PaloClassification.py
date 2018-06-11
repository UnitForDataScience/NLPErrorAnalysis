import os
import pandas as pd

path = './Palo'

textFiles = os.listdir(path)
textToRead = pd.read_csv('./palo.csv')

dictionary = {}
for index, item in textToRead.iterrows():
    dictionary[str(item[0])] = str(item[3])

new_dict = {}
documents = []
targets = []
for file in os.listdir(path):
    check = file.split('R')[0]
    if check in dictionary.keys():
        documents.append(open(path + '/' + file, 'r').read().strip().replace("\n", " "))
        targets.append(check)

print(documents)
print(targets)

from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

text_clf_svm = Pipeline(
    [('vect', CountVectorizer(stop_words="english", min_df=5, ngram_range=(1, 10))),
     ('tfidf', TfidfTransformer(use_idf=True)),
     ('clf-svm', MultinomialNB(alpha=0.05))])
accuracy = []
text_clf_svm.fit(documents, targets)
predict = text_clf_svm.predict(documents)
accuracy.append(np.mean(predict == targets))

print(accuracy)
