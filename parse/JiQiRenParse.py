# -*- coding: utf-8 -*-
from scrapy import Selector


# 机器人 详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@class="articnt"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@class="note")'
                                       u' and not(@class="relative-tag")'
                                       u' and not(@class="cl")'
                                       u' and not(@class="prefer")'
                                       u' and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//ul[@class="author_date"]/li[@class="col-xs-6"]/text()').extract_first(u'')

    # 处理来源
    src_ref = u'机器人网'

    # 处理tags
    tags = response.xpath(u'//div[@class="relative-tag"]/a/text()').extract()
    tags = u','.join(tags)

    # 组装新的内容标签
    content_html = u"""<div class="articnt">
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
