# -*- coding: utf-8 -*-


def in_check(check_list, target_str):
    for check_url in check_list:
        if check_url in target_str:
            return True
    return False


# 找出符合模板的标志
def is_SinaParse(url):
    # http://tech.sina.com.cn/
    # http://finance.sina.com.cn/
    # http://sports.sina.com.cn/
    check_urls = [u'sina.com.cn/']
    return in_check(check_urls, url)


def is_TengXunParse(url):
    # http://tech.qq.com/
    # http://finance.qq.com/
    # http://digi.tech.qq.com/
    # http://new.qq.com/
    check_urls = [u'qq.com/']
    return in_check(check_urls, url)


def is_A5ChuangYeParse(url):
    check_urls = [u'1admin5.com/']
    return in_check(check_urls, url)


def is_CitNewsParse(url):
    check_urls = [u'citnews.com.cn/']
    return in_check(check_urls, url)


def is_CN21TechParse(url):
    check_urls = [u'it.21cn.com/']
    return in_check(check_urls, url)


def is_CnBetaParse(url):
    check_urls = [u'cnbeta.com/']
    return in_check(check_urls, url)


def is_CNQingNianParse(url):
    check_urls = [u'youth.cn/']
    return in_check(check_urls, url)


def is_CnTouZiParse(url):
    check_urls = [u'ocn.com.cn/']
    return in_check(check_urls, url)


def is_CNWangParse(url):
    check_urls = [u'china.com.cn/']
    return in_check(check_urls, url)


def is_DYCJParse(url):
    check_urls = [u'yicai.com/']
    return in_check(check_urls, url)


def is_HeXunParse(url):
    check_urls = [u'hexun.com/']
    return in_check(check_urls, url)


def is_IFengParse(url):
    check_urls = [u'ifeng.com/']
    return in_check(check_urls, url)


def is_ItBearParse(url):
    check_urls = [u'itbear.com.cn/']
    return in_check(check_urls, url)


def is_ITTimesParse(url):
    check_urls = [u'ittime.com.cn/']
    return in_check(check_urls, url)


def is_JinRongJieParse(url):
    check_urls = [u'jrj.com.cn/']
    return in_check(check_urls, url)


def is_JiQiRenParse(url):
    check_urls = [u'roboticschina.com/']
    return in_check(check_urls, url)


def is_Ke36Parse(url):
    check_urls = [u'36kr.com/']
    return in_check(check_urls, url)


def is_KuaiKeJiParse(url):
    check_urls = [u'mydrivers.com/']
    return in_check(check_urls, url)


def is_KuWanParse(url):
    check_urls = [u'kuwankeji.com/']
    return in_check(check_urls, url)


def is_LeiFengParse(url):
    check_urls = [u'leiphone.com/']
    return in_check(check_urls, url)


def is_NanFangParse(url):
    check_urls = [u'southcn.com/']
    return in_check(check_urls, url)


def is_QingDaoParse(url):
    check_urls = [u'qdsdu.com/']
    return in_check(check_urls, url)


def is_RenMinBaseParse(url):
    check_urls = [u'people.com.cn/']
    return in_check(check_urls, url)


def is_TaoGuBaParse(url):
    check_urls = [u'taoguba.com.cn/']
    return in_check(check_urls, url)


def is_TechWebParse(url):
    check_urls = [u'techweb.com.cn/']
    return in_check(check_urls, url)


def is_TomParse(url):
    check_urls = [u'tom.com/']
    return in_check(check_urls, url)


def is_WangYiParse(url):
    # http://tech.163.com/
    # http://money.163.com/
    check_urls = [u'163.com/']
    return in_check(check_urls, url)


def is_XinHuaParse(url):
    check_urls = [u'xinhuanet.com/']
    return in_check(check_urls, url)


def is_XinWenYanParse(url):
    check_urls = [u'xinwen1.com/']
    return in_check(check_urls, url)


def is_ZhongHuaParse(url):
    check_urls = [u'china.com/']
    return in_check(check_urls, url)


def is_ZOLParse(url):
    check_urls = [u'zol.com.cn/']
    return in_check(check_urls, url)
