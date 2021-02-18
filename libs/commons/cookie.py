# coding=utf-8

import re
from libs.commons.data import data

from libs.commons.encode_decode import DEFAULT_ENCODING

class cookie(data):
    def __init__(self, strValues='', encoding=DEFAULT_ENCODING):

        data.__init__(self, encoding=encoding)

        for k, v in re.findall('(.*?)=(.*?);', strValues + ';'):
            k = k.strip()
            v = v.strip()

            self[k] = v

    def _sanitize(self, value):
        value = value.replace('\n', '%0a')
        value = value.replace('\r', '%0d')
        return value

    def __str__(self):
        res = ''
        for parameter_name in self:
            for element_index in xrange(len(self[parameter_name])):
                ks = self._sanitize(parameter_name)
                vs = self._sanitize(self[parameter_name][element_index])
                res += ks + '=' + vs + '; '
        return res[:-1]

