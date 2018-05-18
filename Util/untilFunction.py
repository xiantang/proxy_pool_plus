from Util.WebRequest import WebRequest
import time
from lxml import etree
import requests



def getHtmlTree(url,**kwargs):
    '''
    获取html树
    :param url:
    :param kwargs:
    :return:
    '''
    header={
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    wr=WebRequest()
    time.sleep(2)
    html=wr.get(url=url,header=header).content
    return etree.HTML(html)

def verifyProxyFormat(proxy):

    import re
    varify_regex=r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy=re.findall(varify_regex,proxy)
    return True if len(_proxy)==1 and _proxy[0]==proxy else False

def validUsefulProxy(raw_proxy_dict):
    '''
    检验代理是否可用
    :param proxy:
    :return:
    '''
    # if list(raw_proxy_dict.keys())[0] =='http':

    key=list(raw_proxy_dict.keys())[0]
    proxy=raw_proxy_dict[key]
    if isinstance(proxy,bytes):
        proxy.decode('utf-8')

    proxies={'{}'.format(key):'http://{proxy}'.format(proxy=proxy)}
    try:
        r=requests.get('{}://httpbin.org/ip'.format(key),proxies=proxies,timeout=10,verify=False)
        import re
        new_proxy=re.sub(":\d+", "", proxy)

        if r.status_code==200 and  new_proxy in r.json()['origin']:
            return True

    except Exception as  e:
        return False



