from pyspark import SparkContext
from pyspark import SparkConf
from nltk import sent_tokenize

# Fetching the data from the files
# folderPath = '../Data/'
# files = [open(join(folderPath, f)).read().decode("utf-8").strip() for f in listdir(folderPath) if
#          isfile(join(folderPath, f))]
#
# # Collecting the sentences
# sentences = []
# for file in files:
#     for sentence in sent_tokenize(file):
#         sentences.append(sentence)
# print len(sentences)

# Using Native Spark to do the job as this will scale later
conf = SparkConf().setAppName("Data cleaner").setMaster("local[*]")
sc = SparkContext(conf=conf)

print len(sc.textFile('../Data/').map(lambda x: x.strip())
          .flatMap(lambda x: sent_tokenize(x)).collect())
