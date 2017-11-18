from pyspark import SparkContext
from pyspark import SparkConf
from nltk import sent_tokenize, word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

# Using Native Spark to do the job as this will scale later
conf = SparkConf().setAppName("Data cleaner").setMaster("local[*]")
sc = SparkContext(conf=conf)
lemmatizer = WordNetLemmatizer()

sentences = sc.textFile('../Data/').map(lambda x: x.strip()) \
    .flatMap(lambda x: sent_tokenize(x)).map(lambda x: (x, pos_tag(word_tokenize(x)), word_tokenize(x))).collect()

for (sentence, taggedData, lemmatizedWords) in sentences:
    print '------------------------------------'
    print sentence
    print taggedData
    print tokenizedWords
