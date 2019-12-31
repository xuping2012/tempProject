'''
Created on 2019年10月17日

@author: qguan
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email import encoders
from email.header import Header
import config
from common.HandleLogging import log 
from common.HandleConfig import HandleConfig


class SendEmail(object):
    '''
            封装一个发送邮件的工具类
    '''

    def __init__(self):
        '''
                        初始化工具类的实例对象
        :return:
        '''
        self.logger=log
        self.conf=HandleConfig(config.conf_path+"\\common.conf")
        # 构造smtp服务器连接
        # server.set_debuglevel(1)
        # debug输出模式 默认关闭
        self.server = smtplib.SMTP_SSL(self.conf.get("common", "ALISMTPSERVER"),465)
        
        self.msg = MIMEMultipart()

    def send_email(self,reportFile):
        '''
        发送邮件的方法
        :return:
        '''
        # 发件人姓名与发件箱地址
        self.msg["From"] =self.conf.get("common","From")
        
        # 收件人姓名与收件箱地址
        self.msg["To"] =self.conf.get("common","To")
        
        # 邮件标题
        self.msg["Subject"] = Header("来自SMTP的问候", "utf-8").encode()
        
        #邮件正文
        with open(reportFile, "rb") as f:
            self.msg.attach(MIMEText(f.read(), "html", "utf-8"))

        with open(reportFile, "rb") as f:
        # 设置附件的MIME和文件名
            mime = MIMEBase("html", "html", filename="测试报告.html")
            # 加上必要的头信息
            mime.add_header('Content-Disposition', 'attachment', filename="测试报告.html")
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            self.msg.attach(mime)

        try:
            self.server.login(self.conf.get("common","EmailUser"),self.conf.get("common","EmailSecret"))# 登录smtp服务器
            self.server.sendmail(self.conf.get("common","EmailUser"),self.msg["To"],self.msg.as_string())# 发送邮件
            self.server.quit()
            self.logger.info("发送成功!")
        except Exception as e:
            self.logger.error(str(e))

if __name__ == '__main__':

    sendEmail=SendEmail()
    sendEmail.send_email(reportFile=r"D:\javaworkspace\yasige_online\reports\1576059762.html")