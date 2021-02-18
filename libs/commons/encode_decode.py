# coding=utf-8
'''
encode_decode.py
'''
import re
from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib
import sys

# This pattern matches a character entity reference (a decimal numeric
# references, a hexadecimal numeric reference, or a named reference).
CHAR_REF_PATT = re.compile(r'&(#(\d+|x[\da-fA-F]+)|[\w.:-]+);?', re.U)

UTF8 = 'utf-8'
DEFAULT_ENCODING = UTF8

def htmldecode(text, use_repr=False):
    """
    Decode HTML entities in the given text.

    >>> htmldecode('hola mundo') == 'hola mundo'
    True
    >>> htmldecode(u'hólá múndó') == u'hólá múndó'
    True
    >>> htmldecode(u'hola &#0443') == u'hola \u01bb' ## u'hola ƻ'
    True
    >>> htmldecode(u'hola mundo &#x41') == u'hola mundo A'
    True
    >>> htmldecode(u'&aacute;') == u'\xe1' ## u'á'
    True
    """
    # Internal function to do the work
    def entitydecode(match):
        entity = match.group(1)
        if entity.startswith('#x'):
            return chr(int(entity[2:], 16))

        elif entity.startswith('#'):
            return chr(int(entity[1:]))

        elif entity in name2codepoint:
            return chr(name2codepoint[entity])

        else:
            return match.group(0)

    # "main"
    return CHAR_REF_PATT.sub(entitydecode, text)


def urlencode(query, encoding, safe='%/\<>"\'=:()'):
    '''
    This is my version of urllib.urlencode. It adds "/" as a safe character
    and also adds support for "repeated parameter names".

    Note:
        This function is EXPERIMENTAL and should be used with care ;)

    Original documentation:
        Encode a sequence of two-element tuples or dictionary into a URL query
        string.

        If any values in the query arg are sequences and doseq is true, each
        sequence element is converted to a separate parameter.

        If the query arg is a sequence of two-element tuples, the order of the
        parameters in the output will match the order of parameters in the
        input.


    >>> import cgi
    >>> urlencode(cgi.parse_qs(u'a=1&a=c'), 'latin1')
    'a=1&a=c'
    >>> urlencode(cgi.parse_qs(u'a=1&b=c'), 'latin1')
    'a=1&b=c'
    >>> urlencode(cgi.parse_qs(u'a=á&a=2'), 'latin1')
    'a=%C3%A1&a=2'
    >>> urlencode(u'a=b&c=d', 'utf-8')
    Traceback (most recent call last):
      ...
    TypeError: not a valid non-string sequence or mapping object
    '''

    if hasattr(query, "items"):
        # mapping objects
        query = query.items()
    else:
        # it's a bother at times that strings and string-like objects are
        # sequences...
        try:
            # non-sequence items should not work with len()
            # non-empty strings will fail this
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
            # zero-length sequences of all types will get here and succeed,
            # but that's a minor nit - since the original implementation
            # allowed empty dicts that type of behavior probably should be
            # preserved for consistency
        except TypeError:
            try:
                tb = sys.exc_info()[2]
            finally:
                del tb

    l = []
    is_unicode = lambda x: isinstance(x, unicode)

    if encoding == "gbk":
        encoding = "utf-8"

    for k, v in query:
        # first work with keys
        k = k.encode(encoding) if is_unicode(k) else str(k)
        k = urllib.quote(k, safe)

        if isinstance(v, basestring):
            v = [v]
        else:
            try:
                # is this a sufficient test for sequence-ness?
                len(v)
            except TypeError:
                v = [str(v)]
        for ele in v:
            ele = ele.encode(encoding) if is_unicode(ele) else str(ele)
            l.append(k + '=' + urllib.quote(ele, safe))

    return '&'.join(l)

