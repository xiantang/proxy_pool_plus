import requests
from lxml import etree
from  Util.untilFunction import WebRequest
import re
from Util.untilFunction import getHtmlTree
import sys
sys.path.append('../')

class GetFreeProxy(object):

    def __init__(self):
        pass

    ###############################
    #                             #
    #       HTTP代理               #
    ###############################

    @staticmethod
    def freeProxyFirst(area=33, page=1):
        '''

        :param area: 地区
        :param page: 翻页
        :return:
        '''
        area = 33 if area > 33 else area
        for area_index in range(1, area + 1):
            for i in range(1, page + 1):
                url = 'http://www.66ip.cn/areaindex_{}/{}.html'.format(area_index, i)
                html_tree = getHtmlTree(url)
                tr_list = html_tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    yield tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0]
                break

    @staticmethod
    def freeProxySecond(page_count=2):
        '''
        西刺
        :param page_count:
        :return:
        '''

        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]

        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url=each_url+str(i)
                tree=getHtmlTree(page_url)
                proxy_list=tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in  proxy_list:
                    try:
                        if proxy.xpath('./td[6]/text()')[0] =='HTTP':
                            yield ':'.join(proxy.xpath('./td/text()')[0:2])

                    except Exception as e:
                        pass

    @staticmethod
    def freeProxyThree():
        """
        coderBusy
        https://proxy.coderbusy.com/
        :return:
        """
        urls = ['https://proxy.coderbusy.com/classical/country/cn.aspx?page=1']
        request = WebRequest()
        for url in urls:
            try:
                r = request.get(url)
                proxies = re.findall('data-ip="(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})".+?>(\d+)</td>', r.text)
                for proxy in proxies:
                    yield ':'.join(proxy)
            except Exception as e:
                pass

    @staticmethod
    def freeProxyFour(page=10):
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        :param page: 页数
        :return:
        """
        url_list = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    if ul.xpath('.//li/a/text()')[1]=='http':
                        yield ':'.join(ul.xpath('.//li/text()')[0:2])
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxyFifth():
        """
        guobanjia http://www.goubanjia.com/
        全国代理ip
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                            and not(contains(@style, 'display:none'))
                                            and not(contains(@class, 'port'))
                                            ]/text()
                                    """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '{}:{}'.format(ip_addr, port)
            except Exception as e:
                pass

    @staticmethod
    def freeProxySixth(page_count=9):
        """
        guobanjia http://ip.jiangxianli.com/?page=
        免费代理库
        超多量
        :return:
        """
        for i in range(1, page_count + 1):
                url = 'http://ip.jiangxianli.com/?page={}'.format(page_count)
                html_tree = getHtmlTree(url)
                tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    @staticmethod
    def freeProxySeven():
        '''
        https://www.proxynova.com/proxy-server-list/elite-proxies/
        高匿ip
        :return:
        '''
        url = 'https://www.proxynova.com/proxy-server-list/elite-proxies/'
        html_tree=getHtmlTree(url)
        for i in html_tree.xpath('//*[@id="tbl_proxy_list"]/tbody[1]/tr'):
            try:
                if re.findall('\d+', "".join(i.xpath('./td[@align="left"]/text()'))) != []:
                    ip = i.xpath('./td/abbr/@title')[0]
                    schome = re.findall('\d+', "".join(i.xpath('./td[@align="left"]/text()')))[0]
                    proxy = ip + ':' + schome
                    yield proxy
            except Exception as e:
                pass



    ###############################
    #                             #
    #       HTTPS代理              #
    ###############################

    @staticmethod
    def freeHttpsFirst(page_count=2):

        '''
        HTTPS
        :param page_count:
        :return:
        '''
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url=each_url+str(i)
                tree=getHtmlTree(page_url)
                proxy_list=tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in  proxy_list:
                    try:
                        #//*[@id="ip_list"]/tbody/tr[6]/td[6]
                        if proxy.xpath('./td[6]/text()')[0] =='HTTPS':
                            yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def freeHttpsSecond(page=10):
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        :param page: 页数
        :return:
        """
        url_list = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    if ul.xpath('.//li/a/text()')[1] == 'https':
                        yield ':'.join(ul.xpath('.//li/text()')[0:2])
                except Exception as e:
                    print(e)

    @staticmethod
    def freeHttpsThird():
        '''
        crossin
        http://lab.crossincode.com/proxy/
        :param page_count:
        :return:
        '''

        tree = getHtmlTree('http://lab.crossincode.com/proxy/')
        proxy_list = tree.xpath('//table/tr[position()>1]')
        for proxy in proxy_list:
            try:
                yield proxy.xpath('./td[1]/text()')[0]+ ":" + proxy.xpath("./td[2]/text()")[0]
            except Exception as e:
                print(e)

    @staticmethod
    def freeHttpsFour():
        '''
        crossin
        http://lab.crossincode.com/proxy/
        :param page_count:
        :return:
        '''

        tree = getHtmlTree('https://www.openproxy.co/')
        proxy_list = tree.xpath('//*[@id="featured-2"]/div/div/div[@class="card"]')
        for proxy in proxy_list:
            try:
                yield proxy.xpath('./td[1]/text()')[0] + ":" + proxy.xpath("./td[2]/text()")[0]
            except Exception as e:
                pass

    @staticmethod
    def freeHttpsFive():
        '''
        https://ip.ihuan.me/?page=
        小幻 http代理
        :return:
        '''
        for j in range(1, 30):
            tree = getHtmlTree('https://ip.ihuan.me/?page={}'.format(j))
            for i in tree.xpath('//table/tbody/tr'):
                try:
                    yield i.xpath("./td[1]/a/text()")[0] + ":" + i.xpath("./td[2]/text()")[0]
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    a=getattr(GetFreeProxy,'freeHttpsFive')()
    for i in a:
        print(i)
    # a = getattr(GetFreeProxy, 'freeHttpsSecond')()
    # for i in a:
    #     print(i)