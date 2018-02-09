# -*- coding: utf-8 -*-
from scrapy import Selector
from util import DateUtil


# A5创业网 详情解析
def parse(html):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@class="content"]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style") '
                                       u' and not(@class="sherry_labels")'
                                       u' and not(name(.)="iframe")]|text()')
    if not content_items:
        return None

    date_srf = response.xpath(u'//div[@class="source"]/text()').extract()
    date_srf = u''.join(date_srf).strip()
    date_srf = date_srf.split(u'来源：')

    post_date = u''
    src_ref = u''
    if len(date_srf):
        post_date = date_srf[0]
        post_date = post_date.strip()
        if len(date_srf) > 1:
            src_ref = date_srf[1]
            if not src_ref:
                src_ref = response.xpath(u'//div[@class="source"]/a[@class="source-from"]/text()').extract_first(u'')

    # 处理标题
    title = response.xpath(u'//div[@class="sherry_title"]/h1/text()').extract_first(u'')

    style_in_list = []
    style_need_replace = [
        {u'old': u'#eaeaea', u'new': u'#ffffff'},
    ]

    # 处理作者
    post_user = u''

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div class="content">
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
