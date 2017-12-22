from os import listdir
import pandas as pd

##########################################################
# Documents and their target value
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
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB

accuracy = []

from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

stemit = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()


def stemmer(word):
    # print stemit.stem(word.decode("utf-8"))
    return stemit.stem(word.decode("utf-8"))


text_clf_svm = Pipeline(
    [('vect', CountVectorizer(stop_words="english", min_df=2, ngram_range=(1, 1))),
     ('tfidf', TfidfTransformer(use_idf=True)),
     ('clf-svm', MultinomialNB(alpha=0.05))])
# for i in range(0, 100):

text_clf_svm.fit(documents[0:int(0.6 * len(documents))], target[0:int(0.6 * len(documents))])
predict = text_clf_svm.predict(documents[int(0.6 * len(documents)):len(documents)])
accuracy.append(np.mean(predict == target[int(0.6 * len(documents)):len(documents)]))

print accuracy
