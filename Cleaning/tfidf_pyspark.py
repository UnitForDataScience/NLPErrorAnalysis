from textblob import TextBlob as tb
from pyspark import SparkContext, SparkConf, SQLContext
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
print conf.getAll()
sqlContext = SQLContext(sc)
###############################################
# Making Documents as RDD
###############################################
rddDocuments = sc.parallelize(documents).persist()

##############################################
# This will give all the relevant words in the
# Documents we got
##############################################
wordList = rddDocuments.flatMap(lambda x: x.split(" ")).distinct().filter(
    lambda x: (not x in stop_words) and x.isalpha()).persist()
broadcastedDocuments = sc.broadcast(documents)


##############################################
# This function will help in getting the
# document frequency
##############################################
def df(x):
    ans = 0
    for doc in broadcastedDocuments.value:
        if x in doc:
            ans += 1
    return ans


##############################################
# This function helps in getting the term freq
# for the word in a particular document
##############################################
def termFrequency(x):
    ansArray = []
    docs = broadcastedDocuments.value
    for iter in docs:
        ansArray.append(iter.count(x))
    return ansArray


##############################################
# This function will give tf-idf array of word
# which will later be used in flatmap
##############################################
def tfIDF(x):
    wordTFIDF = []
    for i in range(0, len(x[2])):
        wordTFIDF.append((i, [(x[0], float(x[2][i]) * (562 / (x[1])))]))
    return wordTFIDF


documentTermFrequency = wordList.map(lambda x: (x, float(df(x)), termFrequency(x))).persist() \
    .flatMap(lambda x: tfIDF(x))

filteredTFIDF = documentTermFrequency.filter(lambda x: x[1][0][1] > 30).reduceByKey(lambda x, y: x + y)

tfIDFImportanceArray = {}
for iter in filteredTFIDF.collect():
    tfIDFImportanceArray[iter[0]] = iter[1]

for key,val in tfIDFImportanceArray.iteritems():
    print "-----------------------------------"
    print documents[key]
    print val
    print "-----------------------------------"
