# -*- coding: utf-8 -*-


def in_check(check_list, target_str):
    for check_url in check_list:
        if check_url in target_str:
            return True
    return False


# 找出符合模板的标志
def is_sina(url):
    # http://tech.sina.com.cn/
    # http://finance.sina.com.cn/
    # http://sports.sina.com.cn/
    check_urls = [u'sina.com.cn/']
    return in_check(check_urls, url)


def is_tengxun(url):
    # http://tech.qq.com/
    # http://finance.qq.com/
    # http://digi.tech.qq.com/
    check_urls = [u'qq.com/']
    return in_check(check_urls, url)


def is_tengxun_2(url):
    # http://tech.qq.com/
    # http://finance.qq.com/
    # http://digi.tech.qq.com/
    check_urls = [u'http://new.qq.com/']
    return in_check(check_urls, url)


def is_wangyi(url):
    # http://tech.163.com/
    # http://money.163.com/
    check_urls = [u'163.com/']
    return in_check(check_urls, url)