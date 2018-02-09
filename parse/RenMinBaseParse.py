# -*- coding: utf-8 -*-
from scrapy import Selector
# 人民网 详情解析


def parse(html, source_url=u''):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@id="rwb_zw"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style") '
                                       u'and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    date_srf = response.xpath(u'//div[@class="box01"]/div[@class="fl"]//text()').extract()
    date_srf = u''.join(date_srf).split()

    post_date = u''
    src_ref = u''
    if len(date_srf) >= 1:
        post_date = date_srf[0]
        if len(date_srf) >= 2:
            src_ref = date_srf[1]
            src_ref = src_ref.replace(u'来源：', u'')

    # 处理作者
    post_user = u''.join(response.xpath(u'//p[@class="author"]/text()').extract_first(u'').split())

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""
                    <div class="text_con_left">
                      <div class="src_ref">
                        <div class="box_con">
                             %s
                        </div>
                      </div>
                     </div>
                   """ % (u''.join(content_items.extract()),)

    # 去除不要的标签内容
    clear_paths_in = []
    style_in_list = []
    style_need_replace = [
        {u'old': u'width:660px;', u'new': u''},
        {u'old': u'width:660px', u'new': u''},
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
