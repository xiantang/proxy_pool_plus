import requests

def get_proxy():
    return requests.get("http://127.0.0.1:5050/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.get('http://ip.catr.cn', proxies={"http": "http://{}".format(proxy.decode('utf-8'))})
            # 使用代理访问
            return html.text
        except Exception:

            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    print("删除代理",proxy)
    return None

for i in  range(1,50):
    print(getHtml())