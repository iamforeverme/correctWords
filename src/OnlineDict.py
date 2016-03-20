from urllib2 import urlopen
import re
import webbrowser
import os
import timeit
from scrapy import Selector

class OnlineDict:
    def __init__(self,webSite,dataDir):
        if (isinstance(webSite,list)):
            webSiteList = []
            for item in webSite:
                webSiteList.append(item["url"])
            self.chooseOptWedSite(webSiteList)
        else:
            self.__website = webSite
        self.__dataDir = dataDir

    # Tool function
    def __findContent(self, string, content):
        reStr = re.compile(string)
        m = re.search(reStr, content)
        if m:
            return m.group(0)
        else:
            return None

    def _getMp3Data(self, word,webSite):
        mp3Data = b""
        try:
            articlePageFile = urlopen(webSite.format(word.strip()))
            articleHtml = articlePageFile.read(-1).decode('utf-8')

            sel = Selector(text=articleHtml)
            content = sel.xpath('//span/@data-src-mp3 | //audio/source[1]/source/@src').extract()[0]
            mp3File = urlopen(content)
            mp3Data = mp3File.read()
        except:
            mp3Data = b""
        return mp3Data

    def chooseOptWedSite(self,webSiteList):
        performance = {}
        for website in webSiteList:
            start = timeit.timeit()
            fileName = self._getMp3Data("apple",website)
            end = timeit.timeit()
            if(fileName):
                performance[website] = end - start
                end = 0
                start = 0
        self.__website = min(performance, key=performance.get)
        return self.__website

    def download(self, word):
        mp3Data = self._getMp3Data(word,self.__website)
        if (mp3Data == b""):
            print("word can not be downloaded : " + word)
            return None
        writeFileName = os.path.join(self.__dataDir,word.strip()+".mp3")
        write_file = open(writeFileName, 'wb')
        write_file.write(mp3Data)
        write_file.close()
        return writeFileName

    def pronounce(self, word):
        fileName = os.path.join(self.__dataDir,word.strip()+".mp3")
        if (os.path.isfile(fileName)):
            pass
        else:
            self.download(word)
        webbrowser.open(fileName)
