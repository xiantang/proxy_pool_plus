from DB.RedisClient import RedisClient
from Util.GetConfig import  GetConfig
from ProxyGetter.getFreeProxy import GetFreeProxy
from Util.untilFunction import verifyProxyFormat
from Util.LogHandler import LogHandler
import sys
sys.path.append('../')

class ProxyManage(object):
    '''
    proxymanage
    '''

    def __init__(self):
        self.db=RedisClient('porxy','localhost',6379)
        self.config=GetConfig()
        self.raw_proxy_queue='raw_proxy'
        self.raw_proxy_queue_https='raw_proxy_https'
        self.useful_proxy_queue='useful_proxy'
        self.useful_proxy_queue_https = 'useful_proxy_https'
        self.log=LogHandler('porxy_manager')

    def refresh(self):
        '''
        抓取ip
        https
        http
        :return:
        '''
        self.refresh_mian(self.raw_proxy_queue,
                          self.useful_proxy_queue,
                          self.config.proxy_getter_function)
        self.refresh_mian(self.raw_proxy_queue_https,
                          self.useful_proxy_queue_https,
                          self.config.proxy_getter_https_function)
    def refresh_mian(self,row_table,useful_table,proxy_function):
        '''

        :param row_table: 存原始数据的表
        :param useful_table:可用ip的表
        :param proxy_function:从协议中读取所有可用的方法
        :return:
        '''
        for proxyGetter in proxy_function :
            proxy_set=set()

            try:
                if 'https' in row_table:
                    self.log.info("{func}:fatch Https proxy start".format(func=proxyGetter))
                else:
                    self.log.info("{func}:fatch Http proxy start".format(func=proxyGetter))
                proxy_iter=[_ for _ in getattr(GetFreeProxy,proxyGetter.strip())()]
            except Exception as e:
                self.log.error("{fun}:fetch proxy fail".format(fun=proxyGetter))
                continue
            for proxy in proxy_iter:
                proxy=proxy.strip()
                if proxy and verifyProxyFormat(proxy):

                    self.log.info("{fun}: fetch proxy {proxy}".format(fun=proxyGetter,proxy=proxy))
                    proxy_set.add(proxy)

                else:
                    self.log.error("{fun}: fetch proxy {proxy} error".format(fun=proxyGetter,proxy=proxy))

            for proxy in proxy_set:
                self.db.changeTable(useful_table)
                if self.db.exists(proxy):
                    continue #去重
                self.db.changeTable(row_table)
                self.db.put(proxy)








    def getAll(self,proxy_table):
        '''
        如果是字典列表的话直接返回 如果不是列表就返回字典的键
        :return:
        '''
        self.db.changeTable(proxy_table)
        item_dict=self.db.getAll()
        return item_dict if isinstance(item_dict,list) else list(item_dict.keys())


    def get(self,proxy_table):

        self.db.changeTable(proxy_table)
        item_dict=self.db.get()
        return item_dict if isinstance(item_dict,str)  else item_dict.keys()

    def get_Number(self):
        self.db.changeTable(self.raw_proxy_queue)
        raw_proxy=self.db.get_status()
        self.db.changeTable(self.useful_proxy_queue)
        useful_proxy = self.db.get_status()
        self.db.changeTable(self.raw_proxy_queue_https)
        raw_https_proxy = self.db.get_status()
        self.db.changeTable(self.useful_proxy_queue_https)
        useful_https_proxy = self.db.get_status()
        return {'raw_http_proxy':raw_proxy,'useful_http_proxy':useful_proxy,
                'raw_https_proxy': raw_https_proxy, 'useful_https_proxy': useful_https_proxy}

    def delete(self,proxy):
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy)


if __name__ == '__main__':
    test=ProxyManage()
    print(test.getAll('useful_proxy'))
    print(test.getAll('useful_proxy_https'))
    print(test.get_Number())
    # print(test.getAll('raw_proxy'))
    # print(test.getAll('useful_proxy'))