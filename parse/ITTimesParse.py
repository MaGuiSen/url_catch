# -*- coding: utf-8 -*-
from scrapy import Selector
from util import CssUtil
# IT时代网 详情解析


def parse(html, source_url=u''):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@class="left_main"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@class="toolbp")'
                                       u' and not(@class="toolbar")'
                                       u' and not(@class="interested-article-box")'
                                       u' and not(@class="friend")'
                                       u' and not(@class="changyan_area")'
                                       u' and not(@id="SOHUCS")'
                                       u' and not(@class="mob-author article-author")'
                                       u' and not(@class="shipin")'
                                       u' and not(name(.)="h2") '
                                       u' and not(name(.)="style") '
                                       u' and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = u''

    # 处理来源
    src_ref = u'It时代网'

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div class="article-content">
                             %s
                      </div>
                   """ % (u''.join(content_items.extract()),)
    # 去除不要的标签内容
    clear_paths_in = []
    style_in_list = []
    style_need_replace = [
        {u'old': u'background:#efefef;', u'new': u''},
        {u'old': u'background:#efefef', u'new': u''},
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