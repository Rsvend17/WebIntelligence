from time import sleep
from urllib.robotparser import RobotFileParser

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
seedsRead = open("seeds.txt")

index = {}
crawlcounter = 0
crawleddict = {}

crawlList = []
for line in seedsRead:
    stripped_line = line.strip()
    crawlList.append(stripped_line)

crawledFile = open("crawled.txt", "w")
crawledList = []
for line in crawlList:
    if len(crawledList) < 1000:
        rp = RobotFileParser()
        rp.set_url(line)
        try:
            rp.read()
        except:
            continue
        print(line)
        sleep(2)
        crawlcounter = crawlcounter + 1
        crawleddict[crawlcounter] = line

        r = requests.get(line)
        r_parse = BeautifulSoup(r.text, 'html.parser')
        title = r_parse.find('title').string.strip()
        lower_case = r_parse.getText().lower()
        tokens = nltk.word_tokenize(lower_case)
        tokens = [word for word in tokens if word.isalpha()]
        stop_words = set(stopwords.words('english'))

        ps = nltk.PorterStemmer()
        filtered_sentences = [w for w in tokens if not w in stop_words]

        sentence_stemmed = [ps.stem(w) for w in filtered_sentences]

        for w in sentence_stemmed:
            if w in index:
                for i in range(len(index[w])):
                    if crawlcounter in index[w][i]:
                        index[w][i][crawlcounter] = index[w][i][crawlcounter] + 1
                    elif(i == (len(index[w]) - 1)):
                        index[w].append({crawlcounter: 1})

            else:
                index[w] = [{crawlcounter: 1}]



    # for a in r_parse.find_all('a'):
    #    if a.has_attr("href"):
    #       if a['href'][0:4] == 'http' and not (a['href'] in crawlList or a['href'] + "/" in crawlList):
    #          crawlList.append(a['href'])
    # print(len(crawlList))
    # print("popping:  " + line + " from queue")
    # try:
    #   title = r_parse.find('title').string.strip()
    # except:
    #   crawledFile.write(line + "\n")
    #  continue
    # rawledString  = line + " - "+ title + "\n"
    # crawledFile.write(crawledString)
    # crawledList.append(line)
    # print("crawled: " + str(len(crawledList)))

crawledFile.close()

print(index)
# for item in index['twitter']:
#    print(crawleddict[item])

# rp=RobotFileParser()
# rp.set_url("https://www.aau.dk/")
# rp.read()
# print(rp.can_fetch("*","https://www.aau.dk"))


# r=requests.get('https://www.aau.dk/')
# print(type(r))


# r_parse = BeautifulSoup(r.text, 'html.parser')
# print(r_parse.prettify())

# for a in r_parse.find_all('a'):
#   sleep(1)
#  print(a['href'])
