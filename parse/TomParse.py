# -*- coding: utf-8 -*-
from scrapy import Selector

from util import CssUtil


# TOM 详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@class="news_box_text"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//span[@class="infor_time"]/text()').extract_first(u'')
    post_date = post_date.strip()

    # 处理作者
    post_user = u''

    # 处理来源
    src_ref = response.xpath(u'//div[@class="news_box_infor"]/span[@class="infor_from"]//text()').extract()
    src_ref = ''.join(src_ref).strip()

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div class="news_box_text">
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