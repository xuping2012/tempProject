#!/usr/bin/python3

import unittest
import os
import decimal
import jsonpath
from common.HandleExcel import HandleExcel
from Library.ddt import ddt, data
from common.HandleConfig import conf
from common.HandleRequests import HandleRequests
from common.HandleLogging import log
from common.HandleMySQL import HandleMySQL
from common.HandleParamters import TestData,parameters_handle
import config


data_file_path = os.path.join(config.datas_path, "cases.xlsx")

@ddt
class TestRecharge(unittest.TestCase):
    excel = HandleExcel(data_file_path, "recharge")
    cases = excel.get_datas()
    http = HandleRequests()

    @classmethod
    def setUpClass(cls):
        cls.db = HandleMySQL()
        # 登录，获取用户的id以及鉴权需要用到的token
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", 'user'),
            "pwd": conf.get("test_data", "pwd")
        }
        cls.headers = eval(conf.get("env", "headers"))
        json_data = cls.http(url=url, method="post", data=data,is_json=True, headers=cls.headers)
        # -------登录之后，从响应结果中提取用户id和token-------------
        # 1、用户id
        cls.member_id = jsonpath.jsonpath(json_data, "$..id")[0]
        setattr(TestData, "member_id", str(cls.member_id))
        # 2、提取token
        token_type = jsonpath.jsonpath(json_data, "$..token_type")[0]
        token = jsonpath.jsonpath(json_data, "$..token")[0]
        cls.token_data = token_type + " " + token
        setattr(TestData, "token_data", str(cls.token_data))

    @data(*cases)
    def test_recharge(self, case):
        # ------第一步：准备用例数据------------
        # 拼接完整的接口地址
        url = conf.get("env", "url") + case["url"]
        # 请求的方法
        method = case["method"]
        # 请求参数
        # 判断是否有用户id需要替换
#         if "#member_id#" in case["data"]:
#             # 进行替换
#             case["data"] = case["data"].replace("#member_id#",str(self.member_id))
        case["data"]=parameters_handle(case["data"])
        
        data = eval(case["data"])
        # 请求头
#         headers = eval(conf.get("env", "headers"))
        self.headers["Authorization"] = getattr(TestData, "token_data")
        # 预期结果
        expected = eval(case["expected"])
        # 该用例在表单的中所在行
        row = case["case_id"] + 1
        #获取入参充值金额amount的值
        recharge_money = decimal.Decimal(str(data["amount"]))
        log.info("充值金额为：{}".format(recharge_money))
        
        # ------第二步：发送请求到接口，获取实际结果--------
        if case["check_sql"]:
#             log.info("查询用户{}的余额".format(conf.get("test_data", 'user')))
            sql = case["check_sql"].format(conf.get("test_data", 'user'))
            # 获取取充值之前的余额
            start_money = self.db.get_one(sql)
            log.info("充值前金额：{}".format(start_money))

        result = self.http(url=url, method=method, data=data,is_json=True, headers=self.headers)
        # -------第三步：比对预期结果和实际结果-----
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual((expected["msg"]), result["msg"])
            if case["check_sql"]:
                sql = case["check_sql"].format(conf.get("test_data", 'user'))
                # 获取取充值之后的余额
                end_money = self.db.get_one(sql)
                log.info("充值之后金额为:{}".format(end_money))
                # 进行断言
                self.assertEqual(recharge_money,end_money-start_money)

        except AssertionError as e:
            self.excel.write_file(row=row, column=8, result_status="未通过")
#             log.info("用例：{}--->执行未通过".format(case["title"]))
            raise e
        else:
            self.excel.write_file(row=row, column=8, result_status="通过")
#             log.info("用例：{}--->执行通过".format(case["title"]))


if __name__ == '__main__':
    unittest.main()