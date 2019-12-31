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
class TestWithdraw(unittest.TestCase):
    excel = HandleExcel(data_file_path, "withdraw")
    cases = excel.get_datas()
    http = HandleRequests()
    db = HandleMySQL()

    @classmethod
    def setUpClass(cls):
        # 获取登录用户手机号和密码
        cls.mobile_phone = conf.get("test_data", 'user')
        cls.pwd = conf.get("test_data", "pwd")

    @data(*cases)
    def test_withdraw(self, case):
        # ------第一步：准备用例数据------------
        # 拼接完整的接口地址
        url = conf.get("env", "url") + case["url"]
        # 请求的方法
        method = case["method"]
        # 请求参数
        # 判断是否有用户id需要替换
#         if "#member_id#" in case["data"]:
#             case["data"] = case["data"].replace("#member_id#", str(self.member_id))
#         if "#phone#" in case["data"]:
#             case["data"] = case["data"].replace("#phone#", self.mobile_phone)
#         if "#pwd#" in case["data"]:
#             case["data"] = case["data"].replace("#pwd#", self.pwd)
        case["data"]=parameters_handle(case["data"])
        
        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        
        if case["interface"] !="login":
            headers["Authorization"] = getattr(TestData, "token_data")
        # 预期结果
        expected = eval(case["expected"])
        # 该用例在表单的中所在行
        row = case["case_id"] + 1

        # ------第二步：发送请求到接口，获取实际结果--------
        # 判断是否需要sql校验
        if case["check_sql"]:
            sql = case["check_sql"].format(conf.get("test_data", 'user'))
            # 获取取充值之前的余额
            start_money = self.db.get_one(sql)
        # 发送请求，获取结果
        result = self.http(url=url, method=method, data=data,is_json=True, headers=headers)
#         result = response.json()
        if case["interface"] == "login":
            # -------如果是登录接口，从响应结果中提取用户id和token-------------
            # 1、用户id
            member_id = jsonpath.jsonpath(result, "$..id")[0]
            setattr(TestData,"member_id",str(member_id))
            # 2、提取token
            token_type = jsonpath.jsonpath(result, "$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
#             TestData.token_data = token_type + " " + token
            # 下面这行代码和上面哪行代码是一个意思，都是将token设为类属性
            setattr(TestData,"token_data",token_type + " " + token)

        # -------第三步：比对预期结果和实际结果-----
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual((expected["msg"]), result["msg"])
            # 判断是否需要数据库校验
            if case["check_sql"]:
                sql = case["check_sql"].format(conf.get("test_data", 'user'))
                # 获取取充值之前的余额
                end_money = self.db.get_one(sql)
                recharge_money = decimal.Decimal(str(data["amount"]))
                log.info("取现之前金额为{}\n，取现金额为：{}\n，取现之后金额为{}，".format(start_money, recharge_money, end_money))
                # 进行断言(开始的金额减去结束的金额)
                self.assertEqual(recharge_money, start_money - end_money)

        except AssertionError as e:
            self.excel.write_file(row=row, column=8, result_status="未通过")
#             log.info("用例：{}--->执行未通过".format(case["title"]))
            raise e
        else:
            self.excel.write_file(row=row, column=8, result_status="通过")
#             log.info("用例：{}--->执行通过".format(case["title"]))

if __name__ == '__main__':
    unittest.main()