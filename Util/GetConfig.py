from Util.utilClass import  ConfigParse
import os

class GetConfig(object):

    def __init__(self):
        '''
        获取绝对地址
        '''
        self.pwd=os.path.split(os.path.realpath(__file__))[0]
        self.config_path=os.path.join(os.path.split(self.pwd)[0],'Config.ini')
        self.config_file=ConfigParse()
        self.config_file.read(self.config_path)


    @property
    def proxy_getter_function(self):
        '''

        :return:读取方法名字符串
        '''
        return self.config_file.options("ProxyGetter")

    @property
    def proxy_getter_https_function(self):
        '''

        :return:读取Https的方法名
        '''
        return self.config_file.options('HttpsGetter')

if __name__ == '__main__':
    test=GetConfig()

    print(test.proxy_getter_https_function)