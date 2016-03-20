import unittest
import sys
import tempfile
sys.path.append("..")
from src.OnlineDict import OnlineDict
import shutil
import os

class TestOnlineDict(unittest.TestCase):
    def setUp(self):
        mockWebSite = r"http://dictionary.reference.com/browse/{0}?s=t"
        self.__mockStoreDir = tempfile.mkdtemp()
        self.__dic = OnlineDict(mockWebSite,self.__mockStoreDir)
    def tearDown(self):
        shutil.rmtree(self.__mockStoreDir)

    def testChooseOptWedSite(self):
        websiteList = [r"http://dictionary.reference.com/browse/{0}?s=t",
                                     r"http://dictionary.cambridge.org/us/dictionary/english/{0}"]
        self.assertTrue(self.__dic.chooseOptWedSite(websiteList) in websiteList)
    def testDownload(self):
        fileName = self.__dic.download('bread')
        self.assertTrue(os.path.exists(fileName))

    def testPronounce(self):
        self.__dic.pronounce('bread')



if __name__ == '__main__':
    unittest.main()
