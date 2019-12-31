'''
Created on 2019年11月19日
@author: qguan
'''

import unittest
import time
from Library.HTMLTestRunnerNew import HTMLTestRunner
import config

#测试主方法main：

#创建测试套件
suite = unittest.TestSuite()
#加载测试用例
loader=unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(test_register))

# unittest测试框架测试用例以test*开头，discover可以正则匹配py模块文件，忽略大小写
suite.addTest(loader.discover(config.cases_path,pattern="test_soap*"))# pattern默认了匹配"test*"模块的测试用例

# 文件管理器控制
with open(config.reports_path+"report"+str(int(time.time()))+".html", "wb") as pf:
    runner = HTMLTestRunner(stream=pf,  # 打开一个html格式报告文件，将句柄传给stream
                            tester="十年如歌",                    # 报告中示的测试人员
                            description="python24优化login单元测试",        # 报告中显示描述信息
                            title="24期上课的测试报告")                 # 报告中的标题
    runner.run(suite)