'''
Created on 2019年11月25日

@author: qguan
'''

# -*- coding: utf-8 -*-
import os

baseth = os.path.abspath(os.path.dirname(__file__))
#测试用例excel目录
datas_path=os.path.join(baseth+"\\datas\\")
#日志路径
logs_path=os.path.join(baseth+"\\logs\\")
#配置文件路径
conf_path=os.path.join(baseth+"\\properties\\")
#报告路径
reports_path=os.path.join(baseth+"\\reports\\")

music_path=os.path.join(baseth+"\\music\\")
#测试用例目录
cases_path=os.path.join(baseth+"\\testcases\\")


if __name__ == '__main__':
    pass