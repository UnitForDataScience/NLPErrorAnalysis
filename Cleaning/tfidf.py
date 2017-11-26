from textblob import TextBlob as tb
import math
from os import listdir
from os.path import join

path = '../Data'

documents = [tb(open('../Data/' + filename).read().decode("utf-8").strip().replace("\n", " <newline> ")) for filename in listdir(path)]






def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


for i, blob in enumerate(documents):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, documents) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
