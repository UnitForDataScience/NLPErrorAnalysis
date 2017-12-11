from os import listdir
import pandas as pd

##########################################################
# Documents and there target value
##########################################################
path = '../Data'
data = pd.read_csv('../lerresults.csv')
dictionary = {}
for index, item in data.iterrows():
    if str(item[1]) != 'nan':
        dictionary[str(item[0])] = str(item[1])
    else:
        dictionary[str(item[0])] = "boundary"

documents = []
target = []

for document in listdir(path):
    documents.append(open('../Data/' + document).read().strip().replace("\n", "").lower())
    docName = document.split(".csv")[0].split('.txt')[0].split('R00')[0]
    target.append(dictionary[str(docName)])

##########################################################
# TF-IDF Calculations
##########################################################
from sklearn.feature_extraction.text import CountVectorizer

countVector = CountVectorizer()
termFrequency = countVector.fit_transform(documents)

from sklearn.feature_extraction.text import TfidfTransformer

tfIDFTransformer = TfidfTransformer()
tfidf = tfIDFTransformer.fit_transform(termFrequency)

###########################################################
# SVM classifier
###########################################################
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import numpy as np

accuracy = []
text_clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf-svm', SGDClassifier())])
for i in range(0, 100):
    text_clf_svm.fit(documents[0:int(0.70 * len(documents))], target[0:int(0.70 * len(documents))])
    predict = text_clf_svm.predict(documents[int(0.70 * len(documents)):len(documents)])
    accuracy.append(np.mean(predict == target[int(0.70 * len(documents)):len(documents)]))

print accuracy
