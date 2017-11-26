from pyspark import SparkContext
from pyspark import SparkConf
from nltk import sent_tokenize, word_tokenize
from nltk import pos_tag
from nltk import RegexpParser
from nltk import ne_chunk

###########################################################
# Using Native Spark to do the job as this will scale later
###########################################################
conf = SparkConf().setAppName("Data cleaner").setMaster("local[*]")
sc = SparkContext(conf=conf)


##########################################################
# This function will help in chinking the tagged words we
# will use this to remove unnecessary words from the array
##########################################################
def chinker(taggedWords):
    chunkGram = r"""Chunk: {<.*>+}
                            }<CC|CD|EX|FW|IN|DT>+{"""
    chunkParser = RegexpParser(chunkGram)
    chunked = chunkParser.parse(taggedWords)
    chunkedData = [tree for tree in chunked.subtrees() if tree.label() == "Chunk"]
    return chunkedData


########################################################
# This is chunker. You pass all the tags which you want
########################################################
def chunker(taggedWords, chunkGram):
    chunkParser = RegexpParser(chunkGram)
    chunked = chunkParser.parse(taggedWords)
    chunkedData = [tree for tree in chunked.subtrees() if tree.label() == "chunk"]
    return chunkedData


########################################################
# This is the sentence mapper which will do the cleaning
# of the sentence
########################################################
def sentenceMapper(sentence):
    tokenizedWords = word_tokenize(sentence)
    newWordList = []
    for word in tokenizedWords:
        if word.isupper():
            newWordList.append(
                word[0:1].encode("utf-8").upper() + "" + word[1:].encode("utf-8").lower())
        else:
            newWordList.append(word.encode("utf-8"))
    posTagged = pos_tag(newWordList)
    encodedPostTag = [(tagged[0].decode('utf-8'), tagged[1]) for tagged in posTagged]
    relevantChunks = ['chunk: {<NN><NNS>}', 'chunk: {<JJ><NN><NN>}', 'chunk: {<NN><IN><NN>}', 'chunk: {<NN>}',
                      'chunk: {<NNS><NN>}', 'chunk: {<NN><NN>}', 'chunk: {<NN><IN><NN>}', 'chunk: {<NN><NNS>}',
                      'chunk: {<NN><IN><JJ><NN>}', 'chunk: {<NN><IN><VBG><NNS>}', 'chunk: {<JJ><NN>}',
                      'chunk: {<VBN><TO><VB>}', 'chunk: {<JJ><NN>}', 'chunk: {<NN><IN><NN>}', 'chunk: {<NN><IN><VBG>}',
                      'chunk: {<NN><IN><DT><NN><NN><NN>}', 'chunk: {<RB><VBG><JJ><NN><NN>}', 'chunk: {<NN>}',
                      'chunk: {<JJ><NN>}', 'chunk: {<NN><IN><NN><IN><DT><NNS><CC><NNS>}', 'chunk: {<JJ><NN>}',
                      'chunk: {<NN><IN><NN>}', 'chunk: {<JJ><NN><IN><JJ><NN><NNS>}', 'chunk: {<RB><VBN>}',
                      'chunk: {<RB><RB><VB>}', 'chunk: {<RB><JJ>}']
    # chunkedData = []
    # for chunks in relevantChunks:
    #     chunkedData += chunker(encodedPostTag, chunks)
    ans = False

    themantics = ["Performance issues", "poor work quality", "lack of communication", "miscommunication",
                  "personnel error", "crew error", "lack of coordination", "calculation mistakes",
                  "lack of critical thinking", "lack of questioning skills", "inconsistent leadership",
                  "failed to recognized", "cognitive error", "lack of awareness", "lack of understanding",
                  "weakness in the work control process", "not using conservative decision making", "misapplication",
                  "ineffective communication", "lack of consistency with the decisions and actions",
                  "ineffective supervisory", "lack of verification", "inadequate use of human performance tools",
                  "not informed", "not promptly review", "not unsure"]
    for theme in themantics:
        if (theme.lower() in sentence.lower()):
            ans = True
    return (sentence, ans)


sentences = sc.textFile('../Data/').map(lambda x: x.strip()) \
    .flatMap(lambda x: sent_tokenize(x)).map(lambda x: x).map(sentenceMapper).persist()


sentencesListSally = sentences.filter(lambda x: x[1]).map(lambda x: x[0]).collect()
for sentence in sentencesListSally:
    print sentence
