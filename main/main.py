from multiprocessing import Process
from Schedule.ProxyVaildSchedule import  run as ValidRun
from Schedule.ProxyRefreshSchedule import run as ReFreshRun
from api.ProxyApi import run as ApiRun
import sys
sys.path.append('../')

def run():
    p_list=list()
    p2 = Process(target=ValidRun, name='RefreshRun')
    p_list.append(p2)
    p1=Process(target=ReFreshRun,name='ValiRun')
    p_list.append(p1)#记住进程传入的一定是地址
    p3=Process(target=ApiRun ,name="ApiRun")
    p_list.append(p3)

    for p in p_list:
        p.daemon=True
        p.start()
    for p in p_list:
        p.join()

if __name__ == '__main__':
    run()