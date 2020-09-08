import requests
from bs4 import BeautifulSoup
from time import sleep
from urllib.robotparser import RobotFileParser


seedsRead = open("seeds.txt")

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
        r=requests.get(line)
        r_parse = BeautifulSoup(r.text, 'html.parser')
        for a in r_parse.find_all('a'):
            if a.has_attr("href"):
                if a['href'][0:4] == 'http' and not (a['href'] in crawlList or a['href'] + "/" in crawlList):
                    crawlList.append(a['href'])
        print(len(crawlList))
        print("popping:  " + line + " from queue")
        try:
            title = r_parse.find('title').string.strip()
        except:
            crawledFile.write(line + "\n")
            continue
        crawledString  = line + " - "+ title + "\n"
        crawledFile.write(crawledString)
        crawledList.append(line)
        print("crawled: " + str(len(crawledList)))
    


crawledFile.close()



    



#rp=RobotFileParser()
#rp.set_url("https://www.aau.dk/")
#rp.read()
#print(rp.can_fetch("*","https://www.aau.dk"))


#r=requests.get('https://www.aau.dk/')
#print(type(r))


#r_parse = BeautifulSoup(r.text, 'html.parser')
#print(r_parse.prettify())

#for a in r_parse.find_all('a'):
 #   sleep(1)
  #  print(a['href'])