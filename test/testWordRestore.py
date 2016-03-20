import unittest
from tempfile import NamedTemporaryFile
import os
import sys
sys.path.append("..")
from src.WordRestore import SprintReview

def isRightWord(rightCount,reviewCount):
    if(reviewCount == 1 and rightCount ==1):
        return True
    else:
        return False

def isRightWord0(rightCount,reviewCount):
    if(reviewCount == 0 and rightCount ==0):
        return True
    else:
        return False
class TestWordRestore(unittest.TestCase):

    def setUp(self):
        self.__wordConfigFile = NamedTemporaryFile(delete=False)
        self.__wordConfigFile.write("""{"systematic": {"right": 1, "review": 1}, "opposite": {"right": 0, "review": 1}}""")
        self.__wordConfigFile.close()
        self.__dumpWordFileName = NamedTemporaryFile(delete=False)
        self.__dumpWordFileName.close()
        print(os.path.exists(self.__dumpWordFileName.name))
        self.__restorer = SprintReview(self.__wordConfigFile.name,self.__dumpWordFileName.name)

    def tearDown(self):
        os.remove(self.__dumpWordFileName.name)
        os.remove(self.__wordConfigFile.name)

    def testGetReviewList(self):
        wordList = self.__restorer.getReviewList(2,isRightWord)
        self.assertTrue("systematic" in wordList)

    def testReviewFalse(self):
        result = ""
        expectedResult = "opposite"
        self.__restorer.review("opposite",False)
        self.__restorer.recordResult(False)
        with open(self.__dumpWordFileName.name,"r") as fileObj:
           result = fileObj.read()
        self.assertEqual(result,expectedResult)

    def testRecordResult(self):
        expectedResult = "opposite"
        result = ""
        self.__restorer.recordResult(True)
        with open(self.__dumpWordFileName.name,"r") as fileObj:
           result = fileObj.read()
        self.assertEqual(result,expectedResult)

    def testProduceJSON(self):
        wordList = """apple
        head"""
        self.__restorer.produceJSON(wordList)
        wordList = self.__restorer.getReviewList(2,isRightWord0)
        self.assertTrue("apple" in wordList)

if __name__ == '__main__':
    unittest.main()
