from manage.ProxyManager import ProxyManage
from threading import Thread
from Util.untilFunction import validUsefulProxy
from Util.LogHandler import LogHandler
import sys
sys.path.append('../')
FAIL_COUNT = 1


class Proxy_Check_Http(ProxyManage, Thread):

    def __init__(self, queue_http, item_dict):
        ProxyManage.__init__(self)
        Thread.__init__(self)
        self.log = LogHandler('proxy_check')
        self.queue_http = queue_http
        self.item_dict = item_dict

    def run(self):
        '''
        执行函数
        验证http
        :return:
        '''
        self.db.changeTable(self.useful_proxy_queue)
        while self.queue_http.qsize():
            proxy = self.queue_http.get()
            raw_proxy_dict = {
                'http': proxy
            }
            if validUsefulProxy(raw_proxy_dict):

                self.db.put(proxy)

                self.log.info("ProxyCheck :{} validation pass".format(proxy))
            else:
                self.db.delete(proxy)
                self.log.info("ProxyCheck :{} validation delete".format(proxy))

            self.queue_http.task_done()


class Proxy_Check_Https(ProxyManage, Thread):
    def __init__(self, queue_https, item_dict):
        ProxyManage.__init__(self)
        Thread.__init__(self)
        self.log = LogHandler('proxy_check')
        self.queue_https = queue_https
        self.item_dict = item_dict

    def run(self):
        self.db.changeTable(self.useful_proxy_queue_https)
        while self.queue_https.qsize():


            proxy = self.queue_https.get()
            raw_proxy_dict = {
                'https': proxy
            }
            if validUsefulProxy(raw_proxy_dict):

                self.db.put(proxy)

                self.log.info("ProxyCheck :{} validation pass".format(proxy))
            else:
                self.db.delete(proxy)
                self.log.info("ProxyCheck :{} validation delete".format(proxy))

            self.queue_https.task_done()
