# coding=utf-8

import sys
import configs.configs as Settings

import json
import time


class HtmlReport:
    def __init__(self, db_info=None, model="SITE"):
        if model == "SITE":
            self._report_template = "D:\\test_scan\\report\\templates\\WAT_SITE_Report_For_Test_V1.html"
        elif model == "MAPP":
            self._report_template ="D:\\test_scan\\report\\templates\\WAT_MAPP_Report_For_Test_V1.html"

        print(Settings.ROOT_PATH)
        self._report_dir = "D:\\test_scan\\report\\templates"

        self._db_info = db_info

        self._apiinfos = []
        self._vulntypes = []
        self._vulninfos = []
        self._infos = {}

        self._vulnids = []

    def set_report_info(self, target, date_string=""):
        if date_string == "":
            self._infos["date"] = time.strftime('%a %b %d %X %Y', time.localtime(time.time()))
        self._infos["target"] = target

    def generate(self, filename):
        report_dict = json.loads(str(self._db_info))

        json_data = json.dumps(report_dict)

        fd = open(self._report_template, "r+",encoding='utf-8')
        html_data = fd.read()
        html_data = html_data.replace("#___JSON_DATA___#", json_data)
        fd.close()

        filepath = self._report_dir + time.strftime('%Y-%m-%d', time.localtime(time.time())) + "_" + filename
        fd_new = open(filepath, "w+")
        fd_new.write(html_data)
        fd_new.close()
