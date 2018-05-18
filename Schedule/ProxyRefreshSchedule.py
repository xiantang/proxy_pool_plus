from manage.ProxyManager import ProxyManage
import time
from threading import Thread
from Util.untilFunction import validUsefulProxy
from  apscheduler.schedulers.blocking import  BlockingScheduler
from Util.LogHandler import LogHandler
import sys
sys.path.append('../')


class proxyRefreshSchedule(ProxyManage):

    '''
    定期刷新代理
    '''

    def __init__(self):
        ProxyManage.__init__(self)
        self.log=LogHandler("refresh_schedule")

    def validProxy(self,row_table,usefultable):
        '''
        验证row_proxy 中的代理
        :return:
        '''

        self.db.changeTable(row_table)
        raw_proxy_item=self.db.pop()
        self.log.info("ProxyRefreshSchedule:{} start validProxy".format(time.ctime()))
        remaining_proxies=self.getAll(self.useful_proxy_queue)
        while raw_proxy_item:
            try:
                raw_proxy=raw_proxy_item.get('proxy')
            except:
                raw_proxy=raw_proxy_item
            if isinstance(raw_proxy,bytes):
                raw_proxy.decode('utf-8')
            if 'https' in row_table:
                raw_proxy_dict = {
                    'https': raw_proxy
                }
            else:
                raw_proxy_dict = {
                    'http': raw_proxy
                }
            if(raw_proxy not in remaining_proxies and validUsefulProxy(raw_proxy_dict)):
                self.db.changeTable(usefultable)
                self.db.put(raw_proxy)
                self.log.info("ProxyRefreshSchedule:%s validation pass" %raw_proxy)
            else:
                self.log.info("ProxyRefreshSchedule: %s validation fail"%raw_proxy)
            self.db.changeTable(row_table)
            raw_proxy_item=self.db.pop()
            remaining_proxies=self.getAll(row_table)
        self.log.info("ProxyRefreshSchedule:%s  validProxy complete" % time.ctime())


def refreshPool():
    pp=proxyRefreshSchedule()

    pp.validProxy(pp.raw_proxy_queue,pp.useful_proxy_queue)
    pp.validProxy(pp.raw_proxy_queue_https,pp.useful_proxy_queue_https)
def main(process_num=60):
    p=proxyRefreshSchedule()
    p.refresh()
    #获取新代理
    p1=[]
    for num in range(process_num):
        proc=Thread(target=refreshPool,args=())
        p1.append(proc)
    for num in range(process_num):
        p1[num].daemon=True
        p1[num].start()

    for num in range(process_num):
        p1[num].join()

def run():
    main()
    sch=BlockingScheduler()
    sch.add_job(main,'interval',minutes=10)
    sch.start()

if __name__ == '__main__':
    main()
    # # run()
    # pp=proxyRefreshSchedule()
    # pp.validProxy(pp.raw_proxy_queue,pp.useful_proxy_queue)