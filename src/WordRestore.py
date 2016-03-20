from json import JSONDecoder,JSONEncoder




class WordRestore():
    def __init__(self,wordConfigFile,dumpWordFileName):
        self.__dataFile = wordConfigFile
        self.__dumpWordFileName = dumpWordFileName
        self._load()


    def _load(self):
        with open(self.__dataFile,"r") as fileObj:
            fileContent = fileObj.read()
            self._wordMap=JSONDecoder().decode(fileContent)
            self._wrongWordList = []

    def update(self):
        with open(self.__dataFile,"w") as fileObj:
            fileObj.write(JSONEncoder().encode(self._wordMap))
    def _generateWordList_(self,nWords,isRightWord):
        pass

    def getReviewList(self,nWords,isRightWord):
        return self._generateWordList_(nWords,isRightWord)

    def produceJSON(self,fileContent,isAdd=False):
        wordMap = {}
        for line in fileContent.splitlines():
            traitMap = {"review":0,"right":0}
            wordMap[line.strip()] = traitMap
        if(not isAdd):
            with open(self.__dataFile,'w') as fileObj:
                fileObj.write(JSONEncoder().encode(wordMap))
            self._load()
        else:
            for key in wordMap.keys():
                if(key not in self._wordMap.keys):
                    self._wordMap[key] = wordMap[key]

    def review(self,word,isRight):
        self._wordMap[word]['review'] = self._wordMap[word]['review'] +1
        if(isRight):
            self._wordMap[word]['right'] = self._wordMap[word]['right'] +1
        else:
            self._wrongWordList.append(word)

    def recordResult(self,isEntireWrong=False):
        #fileName = os.path.join(self.__dumpWordFileName,time.strftime('%b %d %Y %H_%M',time.localtime(time.time()))+".txt")
        fileName = self.__dumpWordFileName
        with open(fileName,"w") as fileObj:
            dumpList = []
            if(not isEntireWrong):
                dumpList = self._wrongWordList
            else:
                entireWrong = []
                for word in self._wordMap.keys():
                    if(self._wordMap[word]['review'] != self._wordMap[word]['right']):
                        entireWrong.append(word)
                dumpList = entireWrong
            dumpStr = ";".join(dumpList)
            fileObj.write(dumpStr)
        return fileName


class SprintReview(WordRestore):
    def _generateWordList_(self,nWords,isRightWord):
        wordList = []
        for key in self._wordMap.keys():
            if(isRightWord(self._wordMap[key]['right'],self._wordMap[key]['review'])):
                wordList.append(key)
            if(len(wordList)==nWords):
                return wordList
        return wordList