'''
Created on 2019年11月26日
@author: qguan
'''

import unittest
from ddt import ddt,data

#分享给同事的示例

@ddt
class Test(unittest.TestCase):


    @data({"1":1})
    def testName0(self,data):
        c=data['1']
        print(c)
        pass

    @data((1,2))
    def testName1(self,data):
        c=data[1]
        print(c)
        pass
    
    @data([3,4])
    def testName2(self,data):
        c=data[0]
        print(c)
        pass
    
    @data("45")
    def testName3(self,data):
        c=data[0]
        print(c)
        pass
    
    @data([(1,),(2,3)])
    def testName4(self,data):
        c=data[0]
        print(c)
        pass

    @data({5,2,3,4})
    def testName5(self,data):
        c=list(data)
        d=c[0]
        print(d,c)
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()