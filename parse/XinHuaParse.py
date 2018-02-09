# -*- coding: utf-8 -*-
from scrapy import Selector
from util import CssUtil
# 新华网 详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@id="p-detail"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style") '
                                       u'and not(@class="video-url")'
                                       u'and not(@class="lb")'
                                       u'and not(@class="p-tags") '
                                       u'and not(@class="zan-wap") '
                                       u'and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//div[@class="h-info"]/span[@class="h-time"]/text()').extract_first(u'')

    # 处理作者
    post_user = u''

    # 处理来源
    src_ref = response.xpath(u'//em[@id="source"]//text()').extract_first(u'')

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div id="p-detail">
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