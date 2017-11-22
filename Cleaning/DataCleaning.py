from pyspark import SparkContext
from pyspark import SparkConf
from nltk import sent_tokenize, word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk import RegexpParser

# Using Native Spark to do the job as this will scale later
conf = SparkConf().setAppName("Data cleaner").setMaster("local[*]")
sc = SparkContext(conf=conf)
lemmatizer = WordNetLemmatizer()


def chunkExtractor(t):
    print t.node
    return True


def chinker(taggedWords):
    chunkGram = r"""Chunk: {<.*>+}
                            }<CC|CD|EX|FW|IN|DT>+{"""
    chunkParser = RegexpParser(chunkGram)
    chunked = chunkParser.parse(taggedWords)
    chunkedData = [tree for tree in chunked.subtrees() if tree.label() == "Chunk"]
    print chunkedData


def chunker(taggedWords):
    chunkGram = r"""Chunk: {<NNP.?>+}"""
    chunkParser = RegexpParser(chunkGram)
    chunked = chunkParser.parse(taggedWords)
    print chunked


# This is the sentencemapper which will do the cleaning of the sentence
def sentenceMapper(sentence):
    tokenizedWords = word_tokenize(sentence)
    newWordList = []
    for word in tokenizedWords:
        if word.isupper():
            newWordList.append(
                word[0:1].encode("utf-8").upper() + "" + word[1:].encode("utf-8").lower())
        else:
            newWordList.append(word)
    posTagged = pos_tag(newWordList)
    return (sentence, posTagged, newWordList)


sentences = sc.textFile('../Data/').map(lambda x: x.strip()) \
    .flatMap(lambda x: sent_tokenize(x)).map(lambda x: x).map(sentenceMapper)

for (sentence, taggedData, lemmatizedWords) in sentences.collect():
    print '------------------------------------'
    # print sentence
    # print taggedData
    chinker(taggedData)
    raw_input("Press any key to continue")
# print lemmatizedWords
