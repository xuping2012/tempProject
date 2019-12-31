# coding:utf-8
import json
import suds
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import random
from common.HandleMySQL2 import HandleMySQL2


class HandleWebservice:
    '''
            定义一个webservice类型的接口处理类
    '''
    def __init__(self, api_addr):
        '''
                        构造器
        :param api_addr:接口地址
        :param api_name:接口名称
        '''
        imp = Import('http://www.w3.org/2001/XMLSchema',
        location='http://www.w3.org/2001/XMLSchema.xsd')
        imp.filter.add('http://WebXml.com.cn/')
        self.doctor = ImportDoctor(imp)
        self.url = api_addr
        self.client = Client(self.url, doctor=self.doctor)


    def soap_req(self, data, api_name):
        '''
        webservice请求处理方法
        :param data: 字典数据类型的请求体
        :return: json数据格式类型的str
        '''
        try:
            res = "self.client.service.{}({})".format(api_name, data)
            res = eval(res)
            # 类型转换，反序列化，返回json对象
#             res_str = json.dumps(dict(res), ensure_ascii=False)
#             return json.loads(res_str)
        except suds.WebFault as e:
#             res=e
 # 类型转换，反序列化,返回json对象
#             res_str = json.dumps(dict(e.fault), ensure_ascii=False)
#             return json.loads(res_str)
            return dict(e.fault)
        else:
            return dict(res)
    
    
    @staticmethod
    def mobile():
        mobile = "13" + str(random.randint(100000, 999999)) + "321"
        return mobile
    
    
    def __call__(self, data, api_name):
        """第二种方法，类本身"""
        # 获取类对象的方法
        str = getattr(self.client.service, api_name)
        try:
            res = str(data)
        except suds.WebFault as e:
            return dict(e.fault)
        else:
            return dict(res)
        

if __name__ == '__main__':
    # 创建mysql操作对象
    mysql = HandleMySQL2()
    # 发送短信
    url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    soap = HandleWebservice(url)
    phone = soap.mobile()
    data = {"client_ip":"1", "tmpl_id":1, "mobile":phone}
    res = soap(data, "sendMCode")
    print(res)
    # 查询验证码
    sql = "select Fverify_code from sms_db_21.t_mvcode_info_3 where Fmobile_no={}".format(phone)
    Fverify_code = mysql.get_one(sql)
    # 注册
    url1 = 'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
    data1 = {"verify_code":Fverify_code, "user_id":phone, "channel_id":1, "mobile":phone, "pwd":"123", "ip":"11.1.1.1"}
    soap = HandleWebservice(url1)
    res1 = soap.soap_req(data1, "userRegister")
    print(res1)
