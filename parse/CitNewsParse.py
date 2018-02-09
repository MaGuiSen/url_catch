# -*- coding: utf-8 -*-
from scrapy import Selector
from util import CssUtil
# CitNews 详情解析
from util import DateUtil


def parse(html):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@class="newstext"]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return None

    # 处理时间
    post_date = response.xpath(u'//div[@class="source"]/span[@class="time"]/text()').extract_first(u'')

    title = response.xpath(u'//meta[@property="og:title"]/@content | //title/text()').extract_first(u'')

    style_in_list = []
    style_need_replace = []

    # 处理作者
    post_user = response.xpath(u'//em[@id="source"]//text()').extract_first(u'')

    # 处理来源
    src_ref = response.xpath(u'//div[@class="source"]/text()').extract()
    src_ref = u''.join(u''.join(src_ref).split())
    if u'来源：' in src_ref:
        src_ref = src_ref.replace(u'来源：', '')
    else:
        src_ref = u''

    # 处理tags
    tags = response.xpath(u'//meta[@name="keywords"]/@content').extract_first('')

    # 组装新的内容标签
    content_html = u"""<div class="newstext">
                           %s
                      </div>
                   """ % (u''.join(content_items.extract()),)

    content_item = {
        u'title': title,
        u'content_html': content_html,
        u'post_date': post_date,
        u'style_in_list': style_in_list,
        u'style_need_replace': style_need_replace,
    }

    return content_item


if __name__ == '__main__':
    pass