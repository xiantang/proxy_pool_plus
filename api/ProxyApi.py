# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""

-------------------------------------------------
   File Name：     ProxyApi.py
   Description :
   Author :       JHao
   date：          2016/12/4
-------------------------------------------------
   Change Activity:
                   2016/12/4:
-------------------------------------------------
"""
__author__ = 'JHao'


from werkzeug.wrappers import Response
from flask import Flask, jsonify, request
import sys
sys.path.append('../')

from Util.GetConfig import GetConfig
from manage.ProxyManager import ProxyManage

app = Flask(__name__)


class JsonResponse(Response):

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)


app.response_class = JsonResponse

api_list = {
    'get_http': 'get one HTTP proxy',
    'get_https': 'get one HTTPS proxy',
    'get_all_http': 'get all HTTP proxy',
    'get_all_https': 'get all HTTPS proxy',
    'get_status': 'get proxy pool\'s current status'
}


@app.route('/')
def index():
    '''
    首页
    :return:
    '''
    return api_list


@app.route('/get_all_http/')
def get_all_http_():
    '''
    获取全部http
    :return:
    '''
    proxies = ProxyManage().getAll('useful_proxy')
    return proxies


@app.route('/get_all_https/')
def get_all_http():
    '''
    获取全部https
    :return:
    '''
    proxies = ProxyManage().getAll('useful_proxy_https')
    return proxies


@app.route('/get_http/')
def get_http():
    '''
    获取一个http
    :return:
    '''
    proxy = ProxyManage().get('useful_proxy')
    return proxy if proxy else "no proxy"


@app.route('/get_https/')
def get_https():
    '''
    获取一个https
    :return:
    '''
    proxy = ProxyManage().get('useful_proxy_https')
    return proxy if proxy else "no proxy"


@app.route('/get_status/')
def getStatus():
    '''
    获取数据库状态
    :return:
    '''
    status = ProxyManage().get_Number()
    return status


def run():
    # config = GetConfig()
    app.run(host='127.0.0.1', port=5050)


if __name__ == '__main__':
    run()
