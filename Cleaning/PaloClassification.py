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
        targets.append(dictionary[check])

from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

countVector = CountVectorizer(stop_words="english", min_df=2, ngram_range=(1, 10))
termFrequency = countVector.fit_transform(documents)

tfIDFTransformer = TfidfVectorizer(stop_words="english", min_df=2, ngram_range=(1, 10))
tfIDFTransformer.fit_transform(documents)
for i in tfIDFTransformer.get_feature_names():
    print(i)

text_clf_svm = Pipeline(
    [('vect', CountVectorizer(stop_words="english", min_df=2, ngram_range=(1, 10))),
     ('tfidf', TfidfTransformer(use_idf=True)),
     ('clf-svm', SGDClassifier(alpha=0.05, n_iter=10))])
accuracy = []
text_clf_svm.fit(documents[0:int(0.8 * len(documents))], targets[0:int(0.8 * len(documents))])
predict = text_clf_svm.predict(documents[int(0.6 * len(documents)):len(documents)])
accuracy.append(np.mean(predict == targets[int(0.6 * len(documents)):len(documents)]))
print(predict)
print(accuracy)
