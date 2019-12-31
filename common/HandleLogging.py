'''
# -*- encoding=utf-8 -*-
Created on 2019年11月25日上午10:30:18
@author: qguan
@file:InterFaces.librLibrarydleLog.py

'''
# import logging
import logging.handlers
import config

class HandleLogging(object):
    '''日志收集器工具类'''
    
    #日志输出格式
    formatter='%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        
    def __init__(self,log_file):
        '''
                        初始化日志收集器对象
        '''
#         初始化实例属性
        self.log_file=log_file
        # 创建日志收集器
        self.logger = logging.getLogger()
        # 设置日志收集器的等级，这个我理解成等级总开关，如果到终端的日志没有设置等级以这个设置为准
        self.logger.setLevel("DEBUG") 
        #添加输出通道，控制台或者输出到文件
        self.out_console = logging.StreamHandler()
#         self.out_file = logging.FileHandler(self.log_file,encoding="utf8")
        #按文件大小轮转
        self.out_file=logging.handlers.RotatingFileHandler(filename=self.log_file,mode='a',maxBytes=1024*1024*1024, backupCount=10,encoding="utf8")#maxBytes字节*1024=kb*1024=mb*1024=gb
        #按时间来轮转when时间，interval频次
#         self.out_file=logging.handlers.TimedRotatingFileHandler(filename=self.log_file,backupCount=5,when="D",interval=1)
        # 设置实际日志输出等级
        self.out_console.setLevel("ERROR")
        self.out_file.setLevel("DEBUG")
        #将输出渠道绑定到日志收集器上
        self.logger.addHandler(self.out_console)
        self.logger.addHandler(self.out_file)
        # 创建一个日志输出格式,在类中定义一个类属性，可以为了日志信息的灵活输出，可以在配置文件中定义便于修改
        formatter = logging.Formatter(self.formatter)
        self.out_console.setFormatter(formatter)
        self.out_file.setFormatter(formatter)
        
    def getLog(self):
        '''返回日志收集器对象'''
        return self.logger


#在这里创建一个类对象，便于到工具类的时候直接导入logger即可，不用再创建
log=HandleLogging(log_file=config.logs_path+"server.log").getLog()

if __name__ == '__main__':
#     log=HandleLogging(log_file="server.log").getLog()
    log.debug("这个是自己记录了的debug等级的日志")
    log.info("这个是自己记录了的info等级的日志")
    log.warning("这个是自己记录了的warning等级的日志")
    log.error("这个是自己记录了的error等级的日志")
    log.critical("这个是自己记录了的critical等级的日志")