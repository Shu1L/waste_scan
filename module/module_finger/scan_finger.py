# coding=utf-8

import os
import sys

import re
import json
import hashlib

from httpx.URL import URL
from httpx.curls import wcurl


class FingerScan:
    def __init__(self):
        self._app_file = 'dict.db'
        # 指纹扫描模式:0为根域名扫描；1为自定义路径扫描模式
        self._scan_mode = 0
        self._app_db = open(self._app_file, "rb").readlines()
        self._server_finger = None
        self._http_code = None

    def md5(self, content):
        if isinstance(content, str):
            content = content.encode("utf-8")
        else:
            content = content
        m = hashlib.md5()

        try:
            m.update(content)
            return m.hexdigest()
        except:
            return None

    def set_mode(self, mode):
        self._scan_mode = mode

    # {"wordpress":{"url":"/wp-admin.php","header":("server":"WAF/2.0"),"md5":"aaaaaaaaaaa"}}
    def scan_finger(self, site):
        app_name_list = []
        for item in self._app_db:
            if item.startswith(b"#"):
                continue
            dict_item = json.loads(item.strip())
            app_name = "".join(dict_item.keys()).strip()
            app_info = dict_item.get(app_name)
            url = app_info.get("url")

            urlobj =URL(site)
            if self._scan_mode == 1:
                test_url = urlobj.get_uri_string()
                if test_url.endswith("/"):
                    target_url = test_url[0:-1] + url
                else:
                    target_url = test_url + url
            else:
                test_url = urlobj.get_netloc()
                target_url = urlobj.get_scheme() + "://" + test_url + url
            try:
                res = wcurl.get(target_url)
            except:
                continue
            dst_headers = res.headers
            dst_body = res.body
            self._http_code = res.get_code()
            try:
                self._server_finger = dst_headers["server"]
            except:
                pass
            if dst_body is None:
                continue

            md5_body = self.md5(dst_body)

            key_list = app_info.keys()

            if "headers" in key_list:
                app_headers = app_info.get("headers")
                app_key = app_headers[0].lower()
                app_value = app_headers[1]

                if app_key in dst_headers.keys():
                    dst_info = dst_headers.get(app_key)
                    result = re.search(app_value, dst_info, re.I)
                    if result:
                        if "body" in key_list:
                            app_body = app_info.get("body")
                            result = re.search(app_body, dst_body, re.I)
                            if result:
                                app_name_list.append((target_url, app_name))
                        else:
                            app_name_list.append((target_url, app_name))

            elif "body" in key_list:
                app_body = app_info.get("body")
                result = re.search(app_body, dst_body, re.I)
                if result:
                    app_name_list.append((target_url, app_name))

            elif "md5" in key_list:
                app_md5 = app_info.get("md5")
                if app_md5 == md5_body:
                    app_name_list.append((target_url, app_name))

        return app_name_list

    def get_server(self):
        return self._server_finger

    def get_code(self):
        return self._http_code


if __name__ == "__main__":
    fs=FingerScan()
    fs.set_mode(1)
    sites="http://testphp.vulnweb.com/"
    test=fs.scan_finger(sites)
    print(test)
