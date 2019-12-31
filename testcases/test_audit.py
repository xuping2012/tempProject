import unittest
import os
import jsonpath
from Library.ddt import ddt, data
from common.HandleExcel import HandleExcel
from common.HandleMySQL import HandleMySQL
from common.HandleConfig import conf
from common.HandleRequests import HandleRequests
from common.HandleParamters import TestData, parameters_handle
from common.HandleLogging import log as my_log
import config

 
file_path = os.path.join(config.datas_path, "cases.xlsx")

 
@ddt
class TestAudit(unittest.TestCase):
    excel = HandleExcel(file_path, "audit")
    cases = excel.get_datas()
    http = HandleRequests()
    db = HandleMySQL()

 
    @classmethod
    def setUpClass(cls):
        cls.db = HandleMySQL()
        # 登录，获取用户的id以及鉴权需要用到的token
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", 'admin_user'),
            "pwd": conf.get("test_data", "admin_pwd")
        }
        cls.headers = eval(conf.get("env", "headers"))
        json_data = cls.http(url=url, method="post", data=data,is_json=True, headers=cls.headers)
        # -------登录之后，从响应结果中提取用户id和token-------------
        # 2、提取token
        token_type = jsonpath.jsonpath(json_data, "$..token_type")[0]
        token = jsonpath.jsonpath(json_data, "$..token")[0]
        cls.token_data = token_type + " " + token
        setattr(TestData, "token_data", str(cls.token_data))
        
    
    @data(*cases)
    def test_audit(self, case):
        # 拼接完整的接口地址
        url = conf.get("env", "url") + case["url"]
        # 请求的方法
        method = case["method"]
        
        if case["check_sql"]:
            sql=case["check_sql"]
            loan_id=self.db.get_one(sql)
            setattr(TestData, "loan_id", str(loan_id))
        # 请求参数
        # 替换用例参数
        case["data"] = parameters_handle(case["data"])
        
        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(TestData, "token_data")
        
        # 预期结果
        expected = eval(case["expected"])
        # 该用例在表单的中所在行
        row = case["case_id"] + 1
 
        # ------第二步：发送请求到接口，获取实际结果--------
        result = self.http(url=url, method=method, data=data,is_json=True, headers=headers)
        # -------第三步：比对预期结果和实际结果-----
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual((expected["msg"]), result["msg"])

        except AssertionError as e:
            self.excel.write_file(row=row, column=8, result_status="未通过")
            my_log.info("用例：{}--->执行未通过".format(case["title"]))
            raise e
        else:
            self.excel.write_file(row=row, column=8, result_status="通过")
            my_log.info("用例：{}--->执行通过".format(case["title"]))
            
            
if __name__ == '__main__':
    unittest.main()
    pass