'''
Created on 2019年11月19日

@author: qguan
'''

import unittest
from functions.login import login_check
from functions.register import register
from common.HandleExcel import HandleExcel
from Library.ddt import data, ddt 
from common.HandleLogging import log
import config


@ddt
class LoginTestCase(unittest.TestCase):
    '''登录功能测试用例'''

    excel = HandleExcel(config.datas_path + "test.xlsx", sheetname="login")
    cases = excel.get_all_cases()
    
    @data(*cases)
    def test_login(self, case):
        
        log.info("接收测试用例数据")
        param = eval(case["data"])
        expected = eval(case["expected"])
        caseid=case["case_id"]
        
        res = login_check(*param)
        log.info("登录请求结果:{}".format(res))
        
        try:
            self.assertEqual(expected, res)
        except AssertionError as e:
            self.excel.write_file(caseid+1, 5, "不通过")
            log.info("测试用例执行结果:不通过")
            raise e
        else:
            self.excel.write_file(caseid+1, 5, "通过")
            log.info("测试用例执行结果:通过")

@ddt
class RegisterTestCase(unittest.TestCase):
    '''注册功能测试用例'''
    
    excel = HandleExcel(config.datas_path + "test.xlsx", sheetname="register")
    cases = excel.get_datas()
    
    @data(*cases)
    def test_register(self, case):
        
        log.info("接收测试用例数据")
        param = eval(case["data"])
        expected = eval(case["expected"])
#         caseid=case["case_id"]

        res = register(*param)
        log.info("注册请求结果:{}".format(res))
        
        try:
            self.assertEqual(expected, res)
        except AssertionError as e:
            self.excel.write_data(case, "result", "不通过")
            log.info("测试用例执行结果:不通过")
            raise e
        else:
            log.info("测试用例执行结果:通过")
            self.excel.write_data(case, "result", "通过")
    
# 如果直接运行这个文件，就使用unittest中的main函数来执行测试用例
if __name__ == '__main__':
    unittest.main()
