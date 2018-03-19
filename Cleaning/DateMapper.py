import datefinder
import json
import datetime
# for match in datefinder.find_dates(open("./HumanErrors/Arkansas Nuclear One/ML12132A371.txt", "r").read()):
#     print match

from os import listdir
import re
from nltk import sent_tokenize

path = "./HumanErrors/"
dict = {}
for plants in listdir(path):
    dict[plants] = {}
    for file in listdir(path + plants):
        date = ""
        data = open(path + plants + "/" + file, 'r').read()
        # data = re.search('Dear(.+?).', data)
        # print data.group(1)
        # for match in datefinder.find_dates(data):
        #     print str(match) + " " + file + " " + plants + " " + data.replace("\n", "")
        #     elem = raw_input("Is this the date for this IR")
        #     if elem.lower() == 'y':
        #         date = match
        #         break
        # dict[plants][file] = str(date)
        found = False

        for sent in sent_tokenize(data.replace("\n", " ")):
            if 'dear' not in str(sent).lower():
                continue
            sent = str(sent)
            index = sent.lower().find('dear')
            sent = sent[index:]
            index = sent.lower().find(": on")
            sent = sent[index:]

            for match in datefinder.find_dates(sent):
                # print str(match) + " " + file + " " + plants + " " + sent
                # elem = raw_input("Is this the date for this IR")
                elem = 'y'
                if elem.lower() == 'y':
                    found = True
                    date = match
                    break

            if found:
                try:
                    year = int(str(date.year))
                except:
                    year = int(raw_input("enter the year"))

                # if 2018 <= year or year < 1999:
                #     raw_input("Check this:" + file + " " + plants)
                dict[plants][file] = str(date)
                open("dataFinds.json", "w").write(json.dumps(dict, ensure_ascii=False))
                break

open("dataFinds.json", "w").write(json.dumps(dict, ensure_ascii=False))
