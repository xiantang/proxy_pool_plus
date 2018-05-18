import time
from  queue import Queue
from  manage.ProxyManager import ProxyManage
from  Schedule.ProxyCheck import Proxy_Check_Http,Proxy_Check_Https
import sys
sys.path.append('../')
class ProxyValidSchedule(ProxyManage,object):

    def __init__(self):
        ProxyManage.__init__(self)
        self.proxy_http_item=dict()
        self.proxy_https_item=dict()
        self.queue_Http=Queue()
        self.queue_Https=Queue()

    def __validProxy(self,threads=20):
        '''
        验证useful_proxy 代理
        :param threads:
        :return:
        '''
        thread_list=list()
        #
        for index in range(threads):
            thread_list.append(Proxy_Check_Http(self.queue_Http, self.proxy_http_item))
            thread_list.append(Proxy_Check_Https(self.queue_Https,self.proxy_https_item))


        for thread in thread_list:
            thread.daemon=True
            thread.start()

        for thread in thread_list:
            thread.join()


    def putQueue(self):
        '''
        放入队列
        分别是http 和https
        :return:
        '''

        self.db.changeTable(self.useful_proxy_queue)
        self.proxy_http_item=self.db.getAll()
        for item in self.proxy_http_item:
            self.queue_Http.put(item)


        self.db.changeTable(self.useful_proxy_queue_https)
        self.proxy_https_item = self.db.getAll()
        for item in self.proxy_https_item:

            self.queue_Https.put(item)

    def main(self):
        while True:
            if not self.queue_Http.empty() or not self.queue_Https.empty() :
                self.log.info("start valid useful proxy")
                self.__validProxy()
            else:
                self.log.info("Valid Complte ! sleep 2 minutes")

                time.sleep(60*2)
                self.putQueue()


def run():
        p=ProxyValidSchedule()
        p.main()

if __name__ == '__main__':
    run()