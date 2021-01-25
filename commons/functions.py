# coding=utf-8

from httpx.URL import URL
from simhash import Simhash
import copy


def is_contain_list(a_list, b_list):
    '''
    '''
    if not isinstance(a_list, list) or not isinstance(b_list, list):
        return False

    a_len = len(a_list)
    b_len = len(b_list)

    if a_len != b_len:
        return False

    if a_len >= b_len:
        temp = a_list
        a_list = b_list
        b_list = temp

    a_len_real = len(a_list)
    b_len_real = len(b_list)

    # 判断两个List是否相同或包含
    count = 0
    for a in a_list:
        if a in b_list:
            count = count + 1

    if count == a_len_real and count <= b_len_real:
        return True
    else:
        return False


def is_similar_url(url1, url2):
    '''
    :param url1:
    :param url2:
    :return:
    '''
    if not isinstance(url1, URL):
        url1 = URL(url1)

    if not isinstance(url2, URL):
        url2 = URL(url2)

    url1_str = url1.get_uri_string()
    url2_str = url2.get_uri_string()

    qs1 = url1.get_querystring().keys()
    qs2 = url2.get_querystring().keys()

    if url1_str == url2_str and is_contain_list(qs1, qs2):
        # print "%s=%s" % (url1,url2)
        return True
    else:
        return False


def is_similar_page(res1, res2, radio=0.85):
    '''
    '''
    if res1 is None or res2 is None:
        return False

    body1 = res1.body
    body2 = res2.body

    url1 = res1.get_url()
    url2 = res2.get_url()

    simhash1 = Simhash(body1.split())
    simhash2 = Simhash(body2.split())

    calc_radio = simhash1.distance(simhash2)
    print(calc_radio)
    # print "[%s]与[%s]两个页面的相似度为:%s" % (url1,url2,calc_radio)
    if calc_radio > radio:
        return True
    else:
        return False

if __name__ == '__main__':
    url_list = ['http://www.anquanbao.com/',
                'http://www.anquanbao.com/index.php',
                'http://www.anquanbao.com/index.php?a=1',
                'http://www.anquanbao.com/index.php?a=6',
                'http://www.anquanbao.com/index.php?a=102',
                'http://www.anquanba.com/index.php?b=1',
                'http://www.anquanbao.com/index.php?b=5',
                'http://www.anquanbao.com/index.php?a=1&b=1']

    result = []
    temp_list = copy.deepcopy(url_list)
    if len(temp_list) > 1:
        result.append(temp_list[0])
        del temp_list[0]

        for item in temp_list:
            flag = False
            for a in result:
                if is_similar_url(item,a):
                    flag = True
            if not flag:
                result.append(item)
    print("去似去含前的数据:")
    print(url_list)
    print("去似去含后的数据:")
    print(result)

