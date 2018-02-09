# -*- coding: utf-8 -*-

from scrapy import Selector

from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@class="article-content"][1]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//div[@class="tips-info clearfix"]//div[@class="info"]/span[1]/text()').extract_first(u'')

    src_user = response.xpath(u'//div[@class="tips-info clearfix"]//div[@class="info"]/span[3]/text()').extract_first('')
    src_user = src_user.replace(u' ', '').replace(u'\r\n', ' ')
    src_user = src_user.split(u' ')

    src_ref = u''
    post_user = u''
    # 处理作者
    if len(src_user):
        src_ref = src_user[0]
        if len(src_user) > 1:
            post_user = src_user[1]

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div class="content-box">
                        <div class="article-content">
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
        {u'old': u'background:#333;', u'new': u''},
        {u'old': u'background:#333', u'new': u''},
        {u'old': u'width:620px;;', u'new': u''},
        {u'old': u'width:620px', u'new': u''}
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