# -*- coding: utf-8 -*-
import json

import demjson
from scrapy import Selector
from util import CssUtil
# 新闻眼 详情parse
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@class="content martop20"][1]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script")]|text()')
    if not content_items:
        return

    date_srf_str = response.xpath(u'//div[@class="article"]/div[@class="info"]//text()').extract_first(u'').strip()
    date_srf_str = date_srf_str.split(u'来源于：')

    post_date = ''
    if len(date_srf_str):
        post_date = date_srf_str[0]

    # 处理作者
    post_user = response.xpath(u'//*[@id="author_ename"]/a/text()').extract_first(u'')

    # 处理来源
    src_ref = u''
    if len(date_srf_str) == 2:
        src_ref = date_srf_str[1]

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div class="article">
                        <div class="content">
                             %s
                        </div>
                      </div>
                   """ % (u''.join(content_items.extract()),)

    # 去除不要的标签内容
    clear_paths_in = []
    style_in_list = []
    style_need_replace = [
        {u'old': u'overflow-x:hidden', u'new': u''},
        {u'old': u'overflow:hidden', u'new': u''},
    ]

    title = response.xpath(u'//meta[@property="og:title"]/@content | //title/text()').extract_first(u'')

    content_item = {
        u'title': title,
        u'content_html': content_html,
        u'post_date': post_date,
        u'style_in_list': style_in_list,
        u'style_need_replace': style_need_replace,
        u'clear_paths_in': clear_paths_in
    }

    return content_item


if __name__ == '__main__':
    pass