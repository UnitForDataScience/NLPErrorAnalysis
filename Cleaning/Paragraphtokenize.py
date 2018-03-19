import os
from nltk import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

path = "/home/shanky/workspace/NLPErrorAnalysis/Cleaning/HumanErrors/"
plants = os.listdir(path)

for plant in plants:
    print("------------------------------------");
    print(plant)
    tfIDFdocs = []
    reports = os.listdir(path + plant + "/")
    for report in reports:
        content = open(path + plant + "/" + report, 'rb').read()
        content = ''.join([chr(i) if i < 256 else '' for i in content])
        #print(content)
        data = sent_tokenize(content)

        counter = 0
        found = False
        for sent in data:
            if "human error" in sent.lower() or "human performance" in sent.lower():
                found = True
            counter += 1
            if found:
                break
        if ("cross-cutting" not in data[counter - 1]):
            continue

        string = ""
        string = string + " " + data[counter - 1]
        tfIDFdocs.append(string)

    removeList = stopwords.words("english") + ["human"
        , "performance", "cross", "cutting", "inspectors", "entergy", "nuclear", "safety", "aspect", "finding",
                                               "related", "area"]

    tfidf_vectorizer = TfidfVectorizer(min_df=0.1, max_features=100, stop_words=removeList,
                                       ngram_range=(2, 3))
    tfidf = tfidf_vectorizer.fit_transform(tfIDFdocs)
    tfidfFeatureNames = tfidf_vectorizer.get_feature_names()

    print(tfidfFeatureNames)
