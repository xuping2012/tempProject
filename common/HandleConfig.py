'''
Created on 2019年9月29日
@author: qguan
'''

from  configparser import ConfigParser
import config
from common.HandleLogging import log

class HandleConfig(ConfigParser):

    def __init__(self,file_name,encoding="utf-8"):
        '''初始化读取配置文件，实例化文件参数'''
        super().__init__()
        self.file_name=file_name
        self.encoding=encoding
        self.read(self.file_name,encoding=self.encoding)
    
    def set_section_option_value(self,section,option,value):
        '''设置section：option的值'''
        if not self.has_section(section):
            log.info("{}不存在，需要新增".format(section))
            self.add_section(section)
            self.set(section, option, value)
            self.write(open(self.file_name,"w",encoding=self.encoding))
        else:
            self.set(section, option, value)
            self.write(open(self.file_name,"w",encoding=self.encoding))


conf=HandleConfig(file_name=config.conf_path+'common.conf')
        
if __name__ == '__main__':
    
    confs=HandleConfig(file_name=config.conf_path+'common.conf')
    confs.set_section_option_value("common2", "formatter2", "123")
    res=confs.getint("common2", "formatter1")
    print(res)
#     confs.add_section("success")
#     confs.set_section_value("success12","result","failed")
#     confs.remove_section("success","result")
#     url=confs.get_value("swaggerUrl","base_url")
#     for i in url.split(","):
#         print(i)
#     pass
        