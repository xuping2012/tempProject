# coding:utf-8

import  pymysql
from common.HandleLogging import log
from common.HandleConfig import HandleConfig
import config

conf=HandleConfig(file_name=config.conf_path+"soap.ini")

'''
数据库操作公共类
mysql_info = {"host": '120.55.xxx.xx',
              "port": 3306,
              "user": 'root',
              "passwd": 'xxxx',
              "db": 'xxx',
              "charset": 'utf8'}
'''
# mysql_info = {"host": '120.78.128.25',# test.lemonban.com
#               "port": 3306,
#               "user": 'future', #test
#               "passwd": '123456',#test
#               "db": '',
#               "charset": 'utf8'}

class HandleMySQL2():
    '''
    mysql数据库相关操作
    连接数据库信息：mysql_info
    创建游标：mysql_execute
    查询某个字段对应的字符串：mysql_getstring
    查询一组数据：mysql_getrows
    关闭mysql连接：mysql_close
    '''
    def __init__(self):
#         self.db_info = mysql_info
#         self.conf=HandleConfig(config.conf_path+"common.conf")
        u'''连接池方式'''
        self.conn = HandleMySQL2.__getConnect()#self.db_info

    @staticmethod
    def __getConnect():
        '''静态方法，从连接池中取出连接'''
        try:
            conn = pymysql.connect(host=conf.get("mysql","host"),
                                   port=conf.getint("mysql","port"),
                                   user=conf.get("mysql","user"),
                                   passwd=conf.get("mysql","passwd"),
                                   charset="utf8")
#                                    host=db_info['host'],
#                                    port=db_info['port'],
#                                    user=db_info['user'],
#                                    passwd=db_info['passwd'],
#                                    db=db_info['db'],
#                                    charset=db_info['charset']
            log.info("MySQL数据库连接成功!")
            return conn
        except Exception as a:
            log.error("数据库连接异常：{}".format(a))

    def mysql_execute(self, sql):
        '''执行sql语句'''
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            self.conn.rollback()         # sql执行异常后回滚
            log.error("执行SQL语句出现异常：%s"%a)
        else:
            cur.close()
            self.conn.commit()          # sql无异常时提交
            

    def mysql_getrows(self, sql):
        ''' 返回查询结果'''
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            print("执行SQL语句出现异常：%s"%a)
        else:
            rows = cur.fetchall()
            cur.close()
            self.conn.commit()  
            return rows


    def get_one(self, sql):
        '''查询某个字段的对应值'''
        rows = self.mysql_getrows(sql)
        if rows != None:
            for row in rows:
                for i in row:
                    return i


    def count(self,sql):
        self.conn.commit()
        cur = self.conn.cursor()
        res=cur.execute(sql)
        return res
    
    
    def mysql_close(self):
        ''' 关闭 close mysql'''
        try:
            self.conn.close()
        except Exception as a:
            print("数据库关闭时异常：%s"%a)


if __name__ == "__main__":
    conn=HandleMySQL2()
    res=conn.get_one("select Fverify_code from sms_db_21.t_mvcode_info_3 where Fmobile_no=13784961321")
    print(res)
    conn.mysql_close()