# -*- coding: utf-8 -*-
from scrapy import Selector

from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@id="content"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(name(.)="style") '
                                       u' and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//span[@id="pubtime_baidu"]/text()').extract_first(u'')

    # 处理作者
    post_user = u''.join(response.xpath(u'//span[@id="author_baidu"]//text()').extract())
    post_user = post_user.replace(u'作者：', u'')

    # 处理来源
    src_ref = u''.join(response.xpath(u'//span[@id="source_baidu"]//text()').extract())
    src_ref = src_ref.replace(u'来源：', u'')

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div class="m-article">
                            <div class="content">
                             %s
                            </div>
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