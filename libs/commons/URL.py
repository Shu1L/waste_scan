#coding=utf-8


from urllib import parse
import os
import cgi
import re
import copy
import sys
DEFAULT_ENCODING="utf-8"

class URL:
    def __init__(self,url,encoding=DEFAULT_ENCODING):
        self._already_calculated_url = None
        self._unicode_url=None
        self._changed= False
        self._encoding= encoding
        if not url.startswith("https://") and not url.startswith("http://"):
            url="http://"+url
        urlres=parse.urlparse(url)
        self.scheme=urlres.scheme
        if urlres.port is None:
            self.port=80
        else:
            self.port=urlres.port
        if urlres.netloc.find(":")>-1:
            self.netloc=urlres.netloc
        else:
            self.netloc=urlres.netloc+":"+str(self.port)
        self.path= urlres.path
        self.params=urlres.params
        self.qs=urlres.query
        self.fragment=urlres.fragment

    @classmethod
    def from_parts(cls, scheme, netloc, path, params, qs, fragment, encoding=DEFAULT_ENCODING):
        """
        """
        data = (scheme, netloc, path, params, qs, fragment)
        url_str = parse.urlunparse(data)
        return cls(url_str, encoding)

    def get_domain(self):
        return self.netloc.split(':')[0]

    def get_uri_string(self):
        return URL.from_parts(self.scheme, self.netloc, self.path, None, None, None, encoding=self._encoding).url_string

    def get_netloc(self):
        return self.netloc

    def get_scheme(self):
        return self.scheme

    def get_host(self):
        return self.netloc.split(':')[0]

    def get_port(self):
        return self.port
    def get_querystring(self,ignoreExceptions=True):
        return parse.parse_qs(self.qs, encoding=self._encoding)

    def get_path(self):
        return self.path

    def get_filename(self):
        return self.path[self.path.rfind('/')+1:]

    def get_ext(self):
        fname=self.get_filename()
        ext=fname[fname.rfind('.')+1:]
        if ext==fname:
            return ''
        else:
            return ext

    def get_query(self):
        return self.qs

    def get_fragment(self):
        return self.fragment

    @property
    def url_string(self):
        calc = self._already_calculated_url
        if self._changed or calc is None:
            data = (self.scheme, self.netloc, self.path, self.params, self.qs, self.fragment)
            dataurl =parse.urlunparse(data)
            try:
                calc = str(dataurl)
            except UnicodeDecodeError:
                calc = str(dataurl, self._encoding, 'replace')

            self._already_calculated_url = calc
            self._changed = False

        return str(calc)

    def get_url_string(self):
        return self.url_string

    def urljoin(self, relative):
        jurl = parse.urljoin(self.url_string, relative)
        jurl_obj = URL(jurl, self._encoding)
        return jurl_obj

    def __str__(self):
        return "%s"  % (self.url_string.encode(self._encoding))
    def __repr__(self):
        return '<URL for "%s">' % self.url_string.encode(self._encoding)

