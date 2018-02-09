# -*- coding: utf-8 -*-
from scrapy import Selector
from util import CssUtil
# 中华网详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@id="chan_newsDetail"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    date_srf = response.xpath(u'//div[@id="chan_newsInfo"]/text()').extract()
    date_srf = u' '.join(u''.join(date_srf).split()).split(u'来源：')

    post_date = u''
    src_ref = u''
    post_user = u''
    if len(date_srf) >= 1:
        post_date = date_srf[0]
        if len(date_srf) >= 2:
            src_ref = date_srf[1]

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div id="chan_newsDetail">
                          %s
                       </div>
                   """ % (u''.join(content_items.extract()),)

    # 去除不要的标签内容
    clear_paths_in = []
    style_in_list = []
    style_need_replace = []

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