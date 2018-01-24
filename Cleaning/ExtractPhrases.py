from os import listdir
from nltk import ngrams
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem import SnowballStemmer

ps = SnowballStemmer("english")

stop_words = set(stopwords.words('english'))

path = '../Data'
sentences = []
for document in listdir(path):
    for sent in sent_tokenize(
            open('../Data/' + document).read().decode('utf-8').strip().replace("\n", "").lower()):
        sentences.append(sent)

phrase_counter = Counter()


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


random_stopwords = ["(", ")", "licensee", "event", "report", "nuclear", "\u2022", "nrc", "docker", "ler", "number",
                    "regulatory", "commission", "name", "docket", "day", "month", "year", "continuation", "washington",
                    ",", "dc", "omb", "reported", "lessons", "learned", 'incorporated', 'licensing', 'process', 'fed',
                    'back', 'industry', '.', 'nrc.gov', 'manu-']

for sent in sentences:
    word_tokens = word_tokenize(sent)
    filtered_sentence = [w for w in word_tokens if
                         not hasNumbers(w) and w not in random_stopwords]
    for phrase in ngrams(filtered_sentence, 7):
        phrase_counter[phrase] += 1

most_common_phrases = phrase_counter.most_common(10)
for k, v in most_common_phrases:
    print '{0: <5}'.format(v), k
