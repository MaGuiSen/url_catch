# -*- coding: utf-8 -*-
from from_check import *
from parse import A5ChuangYeParse
from parse import CN21TechParse
from parse import CNQingNianParse
from parse import CNWangParse
from parse import CitNewsParse
from parse import CnBetaParse
from parse import CnTouZiParse
from parse import DYCJParse
from parse import HeXunParse
from parse import IFengParse
from parse import ITTimesParse
from parse import ItBearParse
from parse import JiQiRenParse
from parse import JinRongJieParse
from parse import Ke36Parse
from parse import KuWanParse
from parse import KuaiKeJiParse
from parse import LeiFengParse
from parse import NanFangParse
from parse import QingDaoParse
from parse import RenMinBaseParse
from parse import SinaParse
from parse import TaoGuBaParse
from parse import TechWebParse
from parse import TengXunParse
from parse import TomParse
from parse import WangYiParse
from parse import XinHuaParse
from parse import XinWenYanParse
from parse import ZOLParse
from parse import ZhongHuaParse


def parseContent(url, html):
    content_item = None
    if is_SinaParse(url):
        content_item = SinaParse.parse(html)
    elif is_TengXunParse(url):
        content_item = TengXunParse.parse(html)
    elif is_A5ChuangYeParse(url):
        content_item = A5ChuangYeParse.parse(html)
    elif is_CitNewsParse(url):
        content_item = CitNewsParse.parse(html)
    elif is_CN21TechParse(url):
        content_item = CN21TechParse.parse(html)
    elif is_CnBetaParse(url):
        content_item = CnBetaParse.parse(html)
    elif is_CNQingNianParse(url):
        content_item = CNQingNianParse.parse(html)
    elif is_CnTouZiParse(url):
        content_item = CnTouZiParse.parse(html)
    elif is_CNWangParse(url):
        content_item = CNWangParse.parse(html)
    elif is_DYCJParse(url):
        content_item = DYCJParse.parse(html)
    elif is_HeXunParse(url):
        content_item = HeXunParse.parse(html)
    elif is_IFengParse(url):
        content_item = IFengParse.parse(html)
    elif is_ItBearParse(url):
        content_item = ItBearParse.parse(html)
    elif is_ITTimesParse(url):
        content_item = ITTimesParse.parse(html)
    elif is_JinRongJieParse(url):
        content_item = JinRongJieParse.parse(html)
    elif is_JiQiRenParse(url):
        content_item = JiQiRenParse.parse(html)
    elif is_Ke36Parse(url):
        content_item = Ke36Parse.parse(html)
    elif is_KuaiKeJiParse(url):
        content_item = KuaiKeJiParse.parse(html)
    elif is_KuWanParse(url):
        content_item = KuWanParse.parse(html)
    elif is_LeiFengParse(url):
        content_item = LeiFengParse.parse(html)
    elif is_NanFangParse(url):
        content_item = NanFangParse.parse(html)
    elif is_QingDaoParse(url):
        content_item = QingDaoParse.parse(html)
    elif is_RenMinBaseParse(url):
        content_item = RenMinBaseParse.parse(html)
    elif is_TaoGuBaParse(url):
        content_item = TaoGuBaParse.parse(html)
    elif is_TechWebParse(url):
        content_item = TechWebParse.parse(html)
    elif is_TomParse(url):
        content_item = TomParse.parse(html)
    elif is_WangYiParse(url):
        content_item = WangYiParse.parse(html)
    elif is_XinHuaParse(url):
        content_item = XinHuaParse.parse(html)
    elif is_XinWenYanParse(url):
        content_item = XinWenYanParse.parse(html)
    elif is_ZhongHuaParse(url):
        content_item = ZhongHuaParse.parse(html)
    elif is_ZOLParse(url):
        content_item = ZOLParse.parse(html)
    if content_item:
        print u'有准确的抓取'
    return content_item


if __name__ == '__main__':
    pass
