## All the imports required
import os
from nltk import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

## Place where the inspection reports are kept.
path = "./HumanErrors/"

## Make sure the inspection reports are kept Plant wise.
## Like
## HumanError
##      - Plant Name
##          -- All the txt files
plants = os.listdir(path)

## Stopword list.
removeList = stopwords.words("english") + ["human"
    , "performance", "cross", "cutting", "inspectors", "entergy", "nuclear", "safety", "aspect", "finding",
                                           "related", "area"]
## Reading from one plant at a time.
for plant in plants:
    print("------------------------------------")
    print(plant)
    ## In this we will collect those sentences where "cross cutting aspect of human performance issue" is there
    tfIDFdocs = []
    ## List all the text files in the power plant
    reports = os.listdir(path + plant + "/")
    for report in reports:

        content = open(path + plant + "/" + report, 'rb').read()
        ## The character coding of the txt is not in utf-8 so had to do this step.
        ## This will ensure the coding is utf-8 format. So chars might miss but that
        ## does not remove the important keywords. Only which are unknown.
        content = ''.join([chr(i) if i < 256 else '' for i in content])

        ## Tokeinzing the sentence
        data = sent_tokenize(content)

        counter = 0
        found = False
        for sent in data:
            if "human error" in sent.lower() or "human performance" in sent.lower():
                found = True
            counter += 1
            if found:
                break
        if "cross-cutting" not in data[counter - 1]:
            continue
        # TODO;
        # taking only one sentence where the issue is present
        # Can do better here. Collect all those sentences where
        # issue could be there
        string = ""
        string = string + " " + data[counter - 1]
        tfIDFdocs.append(string)
    # Running tf-idf
    tfidf_vectorizer = TfidfVectorizer(min_df=0.1, max_features=100, stop_words=removeList,
                                       ngram_range=(2, 3))
    tfidf = tfidf_vectorizer.fit_transform(tfIDFdocs)
    tfidfFeatureNames = tfidf_vectorizer.get_feature_names()
    # printing the features
    print(tfidfFeatureNames)
