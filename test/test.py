
import requests
# a=requests.get('http://127.0.0.1:5050/get_all_https/').json()
# for i in a:
#     proxies = {
#         'https': i
#     }
#     print(requests.get('https://httpbin.org/ip',proxies=proxies).text)
import re

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',


}
#https://www.proxyrotator.com/free-proxy-list/3/#free-proxy-list
for j in range(1,151):
    content=requests.get('https://ip.ihuan.me/?page={}'.format(j),headers=headers).text

    from lxml import etree
    selector=etree.HTML(content)
    # lis=[]
    for i in selector.xpath('//table/tbody/tr'):
        ip=i.xpath("./td[1]/a/text()")[0]
        proxy=i.xpath("./td[1]/a/text()")[0]+":"+i.xpath("./td[2]/text()")[0]
        proxies={
                    'https':proxy
                }

        try:
            html=requests.get('https://httpbin.org/ip', proxies=proxies, timeout=3).text
            if ip in html:
                import json
                print(json.loads(html)['origin'])
        except Exception as e:
            print(e)

# try:
#         proxies={
#             'https':'209.141.52.141'
#         }
#
#         print(requests.get('https://httpbin.org/ip',proxies=proxies,timeout=3).text)
# except Exception as e:
#         print(e)