import unittest
import os
import jsonpath
from Library.ddt import ddt, data
from common.HandleExcel import HandleExcel
from common.HandleConfig import conf
from common.HandleParamters import parameters_handle, TestData
from common.HandleRequests import HandleRequests
from common.HandleLogging import log
import config


file_path = os.path.join(config.datas_path, "cases.xlsx")


@ddt
class TestAdd(unittest.TestCase):
    excel = HandleExcel(file_path, "add")
    cases = excel.get_datas()
    http = HandleRequests()
    
    
    @data(*cases)
    def test_add(self, case):
        # 第一步：准备用例数据
        # 获取url
        url = conf.get("env", "url") + case["url"]
        # 获取数据
        case["data"] = parameters_handle(case["data"])
        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "token_data")
        # 预期结果
        expected = eval(case["expected"])
        # 请求方法
        method = case["method"]
        # 用例所在的行
        row = case["case_id"] + 1
        # 第二步：发送请求
        json_data = self.http(url=url, method=method, data=data,is_json=True, headers=headers)
        
        if case["interface"] == "login":
            # 如果是登录的用例，提取对应的token,和用户id,保存为TestData这个类的类属性，用来给后面的用例替换
            token_type = jsonpath.jsonpath(json_data, "$..token_type")[0]
            token = jsonpath.jsonpath(json_data, "$..token")[0]
            token_data = token_type + " " + token
            setattr(TestData, "token_data", token_data)
            id = jsonpath.jsonpath(json_data, "$..id")[0]
            setattr(TestData, "member_id", str(id))
        # 第三步：断言
        try:
            self.assertEqual(expected["code"], json_data["code"])
            self.assertEqual(expected["msg"], json_data["msg"])

        except AssertionError as e:
            self.excel.write_file(row=row, column=8, result_status="未通过")
            log.info("第{}条用例：{}执行失败！".format(row-1,case['title']))
            raise e
        else:
            self.excel.write_file(row=row, column=8, result_status="通过")
            log.info("第{}条用例：{}执行通过！".format(row-1,case['title']))


if __name__ == '__main__':
    unittest.main()
    pass