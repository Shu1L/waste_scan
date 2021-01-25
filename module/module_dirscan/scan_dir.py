# coding=utf-8
import os
import sys
import re
import time
from httpx.curls import wcurl
from module.commons.common import is_404


class DirScan:
	def __init__(self):
		self._found_dir = []
		self._dir_file = None
	def scan_dir(self, site, dir_file=None):
		self._dir_file = 'webdir/web.lst'
		file_list = open(self._dir_file, "r").readlines()
		for item in file_list:
			path = item.strip()
			if path.startswith("#"):
				continue
			if site.endswith("/"):
				url = site[0:-1] + path
			else:
				url = site + path
			res = None
			try:
				res = wcurl.get(url, allow_redirects=False)
				status = res.get_code()
				if status is None:
					break
				msg = "Check URL:" + url + " code:" + str(status)
				if status == 200:
					body = res.text
					if not is_404(body):
						msg = "Found URL:" + url + " code:" + str(status) + " 404 Check: False"
						print(msg)
						self._found_dir.append(url)
				if status == 301 or status == 302:
					next_res = wcurl.get(url, allow_redirects=True)
					if next_res.get_code() == 200:
						body = res.body
						if not is_404(body):
							msg = "Found URL:" + url + " code:" + str(status) + " 404 Check: False"
							print(msg)
							self._found_dir.append(url)
			except Exception as e:
				print("Http Request Error %s" % str(e))

			time.sleep(0.1)

	def get_dir_file(self):
		'''
		'''
		return self._found_dir


if __name__ == "__main__":
	url = 'http://testphp.vulnweb.com'
	print(url)
	dir_scan = DirScan()
	try:
		dir_scan.scan_dir(url)
	except Exception as e:
		print(str(e))
	print("发现的目录和文件:")
	print(dir_scan.get_dir_file())
