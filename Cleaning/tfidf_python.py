from textblob import TextBlob as tb
from pyspark import SparkContext, SparkConf
import math
from nltk.corpus import stopwords
from os import listdir

path = '../Data'

stop_words = set(stopwords.words('english'))

documents = [open('../Data/' + filename).read().decode("utf-8").strip().replace("\n", " <newline> ").lower() for
             filename in
             listdir(path)]

###########################################################
# Using Native Spark to do the job as this will scale later
###########################################################
conf = SparkConf().setAppName("Data cleaner").setMaster("local[*]").set('spark.executor.memory', '14G').set(
    'spark.driver.memory', '45G').set('spark.driver.maxResultSize', '10G').set("spark.executor.heartbeatInterval",
                                                                               "3600s")
SparkContext.setSystemProperty("spark.driver.memory", "40gb")
sc = SparkContext(conf=conf)
nonRDDDocuments = documents
documents = sc.parallelize(documents).persist()


def checkInRDD(x):
    ans = 0
    for iter in nonRDDDocuments:
        if x in iter:
            ans += 1
    print x + " " + str(ans)
    return ans


wordList = documents.flatMap(lambda x: x.split(" ")).distinct().filter(
    lambda x: (not x in stop_words) and x.isalpha()).collect()

idf = []
tf = []
for iter in wordList:
    idf.append((iter, float(562) / float(checkInRDD(iter))))
    tf.append((iter, documents.map(lambda x: x.count(iter))locals().collect()))
print idf



# idf = crossJoined.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y).collect()
# print idf
