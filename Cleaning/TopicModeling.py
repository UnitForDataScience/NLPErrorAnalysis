##########################################################
# Documents and there target value
##########################################################
import pandas as pd
from os import listdir

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


###########################################################
# TF-IDF for NMF model
###########################################################

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

no_features = 1000

tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=0.2, max_features=no_features, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(documents)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

tf_vectorizer = CountVectorizer(max_features=no_features, max_df=0.95, min_df=0.2, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

###########################################################
# LDA and NMF
###########################################################
from sklearn.decomposition import NMF, LatentDirichletAllocation

no_topics = 20
# NMF
nmf = NMF(n_components=no_topics, random_state=1, alpha=0.3, l1_ratio=.5, init='nndsvd').fit(tfidf)

# LDA
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=20, learning_method='online', learning_offset=50,
                                random_state=0).fit(tf)


##########################################################
# displaying topics
##########################################################
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic %d:" % (topic_idx)
        print " ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]])


no_top_words = 10
display_topics(nmf, tfidf_feature_names, no_top_words)

print "####################################################"

display_topics(lda, tf_feature_names, no_top_words)
