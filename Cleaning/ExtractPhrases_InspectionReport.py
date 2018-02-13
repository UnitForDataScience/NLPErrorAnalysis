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
import os

for possible_directory in listdir(file_path):
    possible_sentences = []
    if ".html" in possible_directory:
        continue
    print possible_directory
    os.mkdir("./" + possible_directory)
    inspection_report_path = file_path + possible_directory + "/"
    for file in listdir(inspection_report_path):
        data = _removeNonAscii(open(inspection_report_path + file, 'r').read())
        if "human error" in data.lower() or "human performance" in data.lower():
            open("./" + possible_directory + "/" + file, 'w').write(data)


# with open("sentences.txt", 'w') as f:
#     for s in possible_sentences:
#         f.write(s + '\n')
