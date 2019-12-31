'''
Created on 2019年12月19日

@author: qguan
'''

import unittest
from common.HandleConfig import HandleConfig
from common.HandleExcel import HandleExcel
from common.HandleWebservice import HandleWebservice
from common.HandleParamters import parameters_handle,TestData
from Library.ddt import ddt,data
import config


testcase_path=config.datas_path+"soaptest.xlsx"
conf_path=config.conf_path+"soap.ini"

@ddt
class TestSoap(unittest.TestCase):
    conf=HandleConfig(file_name=conf_path)
    soap=HandleWebservice(conf.get("env","sendsms_url"))
    excel=HandleExcel(filename=testcase_path,sheetname="sendsms")
    cases=excel.get_datas()
    
    @classmethod
    def setUpClass(cls):
        '''参数化手机号'''
        mobile=cls.soap.mobile()
        setattr(TestData, "mobile", mobile)
    
    @data(*cases)
    def test_sendsms(self,case):
#         1，准备数据，替换参数
        data=parameters_handle(case["data"])
        expected=eval(case["expected"])
        row = case["case_id"] + 1
#         2，发送请求
        result=self.soap.soap_req(data,"sendMCode")
        
        try:
#             3，断言，错误码key不一样，需要判断
            if "retCode" in expected.keys():
                self.assertEqual(expected["retCode"], result["retCode"])
                self.assertEqual((expected["retInfo"]), result["retInfo"])
            else:
                self.assertEqual(expected["faultcode"], result["faultcode"])
                self.assertEqual(expected["faultstring"], result["faultstring"])
                
        except AssertionError as e:
            self.excel.write_file(row, 5, result_status="不通过")
            raise e
        else:
            self.excel.write_file(row, 5, result_status="通过")
        
        
if __name__ == '__main__':
    unittest.main()
        
    
        
    