# coding=utf-8


import time
import http.client
import requests
import pandas

from libs.datas.config import cfg
from libs.commons.URL import URL
from libs.commons.Request import Request
from libs.commons.Response import Response, from_requests_response

timeout = 60

DEBUGSWITCH = 1  # 0关闭调试，1开启调试


class wCurl:
    def __init__(self):
        self._time = 0.0
        self._speed = 20
        self._conn = 0
        self._scan_signature = cfg["scan_signature"] if "scan_signature" in cfg else "TScanner/1.0"
        self._scan_cookies = cfg["scan_cookies"] if "scan_cookies" in cfg else {}
        self._scan_proxies = cfg["scan_proxies"] if "scan_proxies" in cfg else {}

        http.client.HTTPConnection.debuglevel = DEBUGSWITCH

    def get_default_headers(self, headers):
        default_headers = {"User-Agent": self._scan_signature}
        default_headers.update(headers)
        return default_headers

    def get(self, url, headers={}, **kwargs):
        default_headers = self.get_default_headers(headers)
        if not isinstance(url, URL):
            url = URL(url)
        requests_response = None
        try:
            requests_response = requests.get(url.url_string,headers=default_headers,**kwargs)
        except:
            return self._make_response(requests_response, url)
        response = self._make_response(requests_response, url)
        return response

    def post(self, url, headers={}, data=None, **kwargs):
        default_headers = self.get_default_headers(headers)
        if not isinstance(url, URL):
            url = URL(url)
        requests_response = None
        try:
            requests_response = requests.post(url.url_string, headers=default_headers, data=data, **kwargs)
        except:
            return self._make_response(requests_response, url)
        response = self._make_response(requests_response, url)
        return response

    def __getattr__(self, name):
        print(name)

    # getattr(requests,name.lower())

    def _send_req(self, req):
        method = req.get_method()
        uri = req.get_url().get_uri_string()
        querystring = req.get_get_param()
        postdata = req.get_post_param()
        headers = req.get_headers()
        cookies = self._scan_cookies
        proxies = self._scan_proxies
        send = getattr(requests, method.lower())
        requests_response = None

        try:
            requests_response = send(uri, params=querystring, data=postdata, headers=headers, cookies=cookies,
                                     proxies=proxies)
        except:
            return self._make_response(requests_response, req.get_url())
        else:
            response = self._make_response(requests_response, req.get_url())
            return response

    def _make_response(self, resp_from_requests, req_url):
        if resp_from_requests is None:
            response = Response(req_url=req_url)
        else:
            response = from_requests_response(resp_from_requests, req_url)
        return response


wcurl=wCurl()

