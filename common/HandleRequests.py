'''
Created on 2019年10月10日

@author: qguan
'''
import requests
import json
from common.HandleLogging import log

class HandleRequests(object):
    '''
            封装一个公共http请求工具类
    '''

    def __init__(self):
        '''
                    构造方法,初始化requests请求方法，为了保持下一个接口请求的headers一致，故而初始为Session
        '''
        self.session = requests.Session()
        self.encoding="utf-8"
    
    def __call__(self, method, url, data=None, is_json=False, **kwargs):
        '''
                        封装一个可以被直接调用的方法
        :param method: 请求方法
        :param url: 请求地址
        :param data: 请求参数
        :param is_json: 如果请求有content-type:application/json，传json格式的数据
        :param kwargs: 占位，可自定义headers还有proxies；爬虫模拟浏览器及代理ip
        :return: 返回一个请求结果
        '''
        # 请求方法的参数转成小写，也可以是大写upper()
        method = method.lower()
        # 判断请求参数是否是str类型的json格式
        if isinstance(data, str):
            try:
                data = json.loads(data) #将json的字符串转成dict
            except Exception as e:
                log.info("str字符串json数据处理异常:{}".format(e))
                if len(data) > 0:
                    data = eval(data)
        # 请求方法
        if method == 'get':
            res = self.session.request(method=method, url=url, params=data, **kwargs)
        elif method in ['post','patch']:
            if is_json:
                res = self.session.request(method=method, url=url, json=data,**kwargs)
            else:
                res = self.session.request(method=method, url=url, data=data, **kwargs)
        else:
            log.info("目前程序暂不支持[{}]该请求方法。".format(method))

        # session需要关闭资源
        self.session.close()
#         httpresponse内容分析有两个文本属性：context和text，如果遇到请求html返回的乱码怎么办？
#         content有decode("utf-8")转码，text需要encode("utf-8").decode("unicode_escape")
#         content返回的是byte 也就是说content自带一个bytes(bytearray(html, encoding='utf-8'))方法。
        res.encoding=self.encoding #结构发现是request返回的编码问题# text返回的是Unicode
        #json.loads(res.text)不确定返回的一定是json，所以还是还原
        #res.json()返回的是json数据，但一定是json格式的，否则会报解析失败
        if is_json:
            return res.json()
        else:
            return res.text 
        
        
if __name__ == '__main__':
    res=HandleRequests()
#     headers={"source": "0",
#              "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiI4ODg5MjgiLCJpc3MiOiIwOThmNmJjZCIsImF1ZCI6InJlc3RhcGl1c2VyIiwianRpIjoiODM0NDkxIn0.2EFdgzo-43zFAnase4u5kx2LobIFBaBF2L95bp968eA",
#              "Content-Type": "application/json; charset=UTF-8"}
#     
#     json_data={"catalog":0,"noteContentId":20,"noteModule":0,"userId":"888928"}
#     
#     url='http://test.user-center.ieltsbro.com/hcp/studyCenter/notebook/getLastNote'
#     
#     print(res("post", url,json_data,is_json=True,headers=headers))
    register_url = "http://api.lemonban.com/futureloan/member/register"
 
    data = '{"mobile_phone": "15867554123","pwd":"123123131","reg_name": "木森","type": 0}'
    print(type(data))
    header = {
       "X-Lemonban-Media-Type": "lemonban.v2",
       "Content-Type": "application/json"
    }
    text=res("post",register_url,data=data,is_json=True,headers=header)
    print(text,type(text))
    