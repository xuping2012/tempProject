# -*- encoding=utf-8 -*-

import unittest
import random
from Library.ddt import ddt,data
from common.HandleExcel import HandleExcel
from common.HandleRequests import HandleRequests
from common.HandleConfig import conf
import config


@ddt
class TestLogin(unittest.TestCase):
    excel=HandleExcel(filename=config.datas_path+"cases.xlsx",sheetname="login")
    cases=excel.get_datas()
    http = HandleRequests()
    
    @data(*cases)
    def test_login(self,case):
        # ------第一步：准备用例数据------------
        # 拼接完整的接口地址
        url = conf.get("env", "url") + case["url"]
        # 请求的方法
        method = case["method"]
        # 请求参数
        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 预期结果
        expected = eval(case["expected"])
        # 该用例在表单的中所在行
        row = case["case_id"] + 1
        # ------第二步：发送请求到接口，获取实际结果--------
        result = self.http(method=method, url=url, data=data,is_json=True, headers=headers)
        # --------------------以下内容为扩展内容----------------
        # 先判断是否注册成功，如果是注册成功
        # self.phone = "注册成功的手机号码"  # 没有注册成功就设置未None
        # ---------------------------------------------------
 
        # -------第三步：比对预期结果和实际结果-----
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual((expected["msg"]), result["msg"])
        except AssertionError as e:
            self.excel.write_file(row=row, column=8, result_status="未通过")
            raise e
        else:
            self.excel.write_file(row=row, column=8, result_status="通过")
        
        
    @staticmethod
    def random_phone():
        """生成随机的手机号码"""
        phone = "131"+str(random.randint(10000000, 99999999))
#         for i in range(8):
#             phone += str(random.randint(0, 9))
        return phone
            
if __name__ == '__main__':
    unittest.main()