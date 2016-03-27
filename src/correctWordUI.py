from Tkinter import *
from WordRestore import SprintReview
from OnlineDict import OnlineDict
from json import JSONDecoder,JSONEncoder
from os import linesep

class Application(Frame):
    def overrideWordList(self):
        data = self.__addContent.get("1.0",END)
        self.__restorer.produceJSON(data,isAdd=False)

    def updateWords(self):
        # add / overwrite current dic
        #self.__startReview.config(state="normal")
        data = self.__addContent.get("1.0",END)
        self.__restorer.produceJSON(data,isAdd=True)


    def startReview(self):
        def isRightWord(rightCount,reviewCount):
            if(reviewCount == int(self.__reviewTimeVar.get()) and rightCount ==int(self.__correctTimeVar.get())):
                return True
            else:
                return False
        self.__wordsList = self.__restorer.getReviewList(2000,isRightWord)
        if(len(self.__wordsList)!=0):
            self.__curWord = self.__wordsList.pop()
            self.__dic.pronounce(self.__curWord)

    def inputDoneCallback(self, event):
        isRight = self.contents.get() == self.__curWord
        self.__restorer.review(self.__curWord,isRight)
        if(isRight):
            self.__resultVar.set("Right!")
        else:
            self.__resultVar.set("Wrong!")
            self.__addContent.insert(END, self.__curWord + linesep)

        if(len(self.__wordsList)!=0):
            self.__curWord = self.__wordsList.pop()
            self.__dic.pronounce(self.__curWord)
        self.contents.set("")
        self.__wordsInput.focus_set()
    def createWidgets(self):
        labelInputNewWords = Label(text="Input words:")
        labelInputNewWords.pack()
        # check if input word is correct
        self.__wordsInput = Entry()
        self.__wordsInput.pack()
        # here is the application variable
        self.contents = StringVar()
        #self.contents.set("input the word")
        self.__wordsInput["textvariable"] = self.contents
        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.__wordsInput.bind('<Key-Return>',
                               self.inputDoneCallback)


        # here is the application variable
        self.__resultVar = StringVar()
        self.__resultVar.set("Result")
        self.__result = Label(textvariable=self.__resultVar)
        self.__result.pack()


        labelCorrectTime = Label(text="Correct Time:")
        labelCorrectTime.pack()
        self.__correctTime = Entry()
        self.__correctTime.pack()



        # here is the application variable
        self.__correctTimeVar = StringVar()
        self.__correctTimeVar.set("0")
        self.__correctTime["textvariable"] = self.__correctTimeVar


        labelReviewTime = Label(text="Review Time:")
        labelReviewTime.pack()
        self.__reviewTime = Entry()
        self.__reviewTime.pack()
        # here is the application variable
        self.__reviewTimeVar = StringVar()
        self.__reviewTimeVar.set("0")
        self.__reviewTime["textvariable"] = self.__reviewTimeVar


        labelNewWords = Label(text="Override/add words:")
        labelNewWords.pack()
        self.__addContent = Text()
        self.__addContent.pack(expand=YES, fill=BOTH)



        self.__pronounce = Button(self)
        self.__pronounce["text"] = "Override Words"
        self.__pronounce["command"] = self.overrideWordList
        self.__pronounce.pack({"side": "left"})

        self.__updateWords = Button(self)
        self.__updateWords["text"] = "Update Words"
        self.__updateWords["command"] = self.updateWords

        self.__updateWords.pack({"side": "left"})

        self.__startReview = Button(self)
        self.__startReview["text"] = "Start review"
        self.__startReview["command"] = self.startReview
        self.__startReview.pack({"side": "left"})


        self.__quit = Button(self)
        self.__quit["text"] = "Quit"
        self.__quit["fg"]   = "red"
        self.__quit["command"] =  self.quit

        self.__quit.pack({"side": "right"})



    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.__configFile = r'../config/config.json'
        with open(self.__configFile,"r") as fileObj:
            fileContent = fileObj.read()
            self.__config=JSONDecoder().decode(fileContent)
        self.__restorer = SprintReview(self.__config["wordJson"],self.__config["dumpTxt"])
        self.__dic = OnlineDict(self.__config["websiteList"],self.__config["wordCache"])

        self.__wordsList = []
        self.__curWord = ""

    def destroy(self):
        self.clearUp()

    def clearUp(self):
        self.__restorer.update()
        self.__restorer.recordResult()
        with open(self.__configFile,'w') as fileObj:
            fileObj.write(JSONEncoder().encode(self.__config))

root = Tk()
app = Application(master=root)
app.mainloop()
try:
    root.destroy()
finally:
    pass