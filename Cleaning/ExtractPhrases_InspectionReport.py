from os import listdir
from collections import Counter
from nltk import ngrams
from nltk import sent_tokenize, word_tokenize
from pyspark import SparkContext, SparkConf

phrase_counter = Counter()
file_path = "../Data/Inspection_Report/"


def _removeNonAscii(s): return "".join(i for i in s if ord(i) < 128)


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


documents = []

for possible_directory in listdir(file_path):
    if '.html' in possible_directory:
        continue
    inspection_report_path = file_path + possible_directory + "/"
    for file in listdir(inspection_report_path):
        documents.append(inspection_report_path + file)
random_stop_words = ["...", 'nrc', 'public']

print documents
# for possible_directory in listdir(file_path):
#     if ".html" in possible_directory:
#         continue
#     inspection_report_path = file_path + possible_directory + "/"
#     print(possible_directory)
#     for file in listdir(inspection_report_path):
#         sentences = sent_tokenize(_removeNonAscii(open(inspection_report_path + file, 'r').read()).lower())
#         for sentence in sentences:
#             filtered_sentence = [w for w in word_tokenize(sentence) if w not in random_stop_words]
#             for phrase in ngrams(filtered_sentence, 10):
#                 phrase_counter[phrase] += 1
#
#     break
#


conf = SparkConf().setAppName("Data cleaner").setMaster("local[*]").set('spark.executor.memory', '14G').set(
    'spark.driver.memory', '160g').set('spark.driver.maxResultSize', '10G').set("spark.executor.heartbeatInterval",
                                                                                "3600s")
SparkContext.setSystemProperty("spark.driver.memory", "40gb")
sc = SparkContext(conf=conf)

phrase_counter = Counter()


def set_phrase_counter(x):
    filtered_sentence = [w for w in word_tokenize(x) if w not in random_stop_words]
    return filtered_sentence


rddDocuments = sc.parallelize(documents).map(
    lambda x: sent_tokenize(_removeNonAscii(open(x, 'r').read()).lower())).map(
    lambda x: [w for w in word_tokenize(x) if w not in random_stop_words]).collect()

#     map(set_phrase_counter).flatMap(lambda x: x).collect()
#
# for item in rddDocuments:
#     phrase_counter[iter] += 1
#
# most_common_phrases = phrase_counter.most_common(1000)
# for k, v in most_common_phrases:
#     print '{0: <5}'.format(v), k
