'''
Created on 2019年12月19日

@author: qguan
'''

import unittest
from common.HandleConfig import HandleConfig
from common.HandleExcel import HandleExcel
from common.HandleWebservice import HandleWebservice
from common.HandleParamters import parameters_handle,TestData
from common.HandleMySQL2 import HandleMySQL2
from Library.ddt import ddt,data
import config


testcase_path=config.datas_path+"soaptest.xlsx"
conf_path=config.conf_path+"soap.ini"

@ddt
class TestSoapRegister(unittest.TestCase):
    conf=HandleConfig(file_name=conf_path)
    soap=HandleWebservice(conf.get("env","register_url"))
    web=HandleWebservice(conf.get("env","sendsms_url"))
    mysql=HandleMySQL2()
    excel=HandleExcel(filename=testcase_path,sheetname="register")
    cases=excel.get_datas()
    phone=web.mobile()
    
    
    @classmethod
    def setUpClass(cls):
        '''参数化手机号'''
#         1，发送短信
        data={"client_ip":"1","tmpl_id":1,"mobile":cls.phone}
        cls.web.soap_req(data,"sendMCode")
        setattr(TestData, "mobile", cls.phone)
#         2，查询验证码
        sql="select Fverify_code from sms_db_21.t_mvcode_info_3 where Fmobile_no={}".format(cls.phone)
        Fverify_code=cls.mysql.get_one(sql)
        setattr(TestData, "verify_code", Fverify_code)
        setattr(TestData, "user_id", cls.phone)
        

    @data(*cases)
    def test_register(self,case):
#         1，准备数据，替换参数
        data=parameters_handle(case["data"])
        expected=eval(case["expected"])
        row = case["case_id"] + 1
#         2，发送请求
        result=self.soap.soap_req(data,"userRegister")
        try:
#             3，断言，错误码key不一样，需要判断
            self.assertEqual(expected["retCode"], result["retCode"])
            self.assertEqual((expected["retInfo"]), result["retInfo"])
        except AssertionError as e:
            self.excel.write_file(row, 5, result_status="不通过")
            raise e
        else:
            self.excel.write_file(row, 5, result_status="通过")
        
            
if __name__ == '__main__':
    unittest.main()
        
    
        
    