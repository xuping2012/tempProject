#-*-coding: UTF-8 -*-
'''
Created on 2019年12月12日

@author: qguan
'''
import re
from common.HandleConfig import conf
from common.HandleLogging import log


class TestData:
    """这个类的作用：专门用来保存一些要替换的数据"""
    pass
 
 
def parameters_handle(data,partten=r"#(.+?)#"):
    '''根据正则匹配参数化，需要替换的参数'''
    
    # 判断是否有需要替换的数据
    while re.search(partten, data):
        # 匹配出第一个要替换的数据
        res = re.search(partten, data)
        # 提取待替换的内容
        item = res.group()
        # 获取替换内容中的数据项
        key = res.group(1)
        try:
            # 根据替换内容中的数据项去配置文件中找到对应的内容，进行替换
            data = data.replace(item, conf.get("test_data", key))
        except:
            try:
                data = data.replace(item, getattr(TestData,key))#要是类中没有这个属性，还是会报错提示类中没这个类属性
            except:
                log.error("TestData类中没有{}类属性".format(key))
                break
    # 返回替换好的数据
    return data

if __name__ == '__main__':
    dic='{"phone":"#phone#","passwd":"#pwd#","name":"#name#","amount":123}'
    res=parameters_handle(dic)
    
    rs=re.match("phone", dic)
    ress=re.search("#(.+?)#", dic)
    print(ress.group(0),ress.group(1),ress.group(0,1))
    pass