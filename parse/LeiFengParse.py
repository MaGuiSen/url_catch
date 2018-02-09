# -*- coding: utf-8 -*-
from scrapy import Selector

from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@class="lph-article-comView"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(name(.)="style")'
                                       u' and not(name(.)="a")'
                                       u' and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//td[@class="time"]/text()').extract_first(u'').strip()

    # 处理作者
    post_user = response.xpath(u'//a[@rel="nofollow"]/text()').extract_first(u'')

    # 处理来源
    src_ref = u'雷锋网'

    # 组装新的内容标签
    content_html = u"""<div class="lphArticle-detail">
                            <div class="lph-article-comView">
                             %s
                           </div>
                      </div>
                   """ % (u''.join(content_items.extract()),)

    content_html = content_html.replace(u'https://static.leiphone.com/uploads/new/category/pic/201801/5a5dd347356f7'
                                        u'.jpg?imageMogr2/thumbnail/!740x140r/gravity/Center/crop/740x140/quality/90'
                                        u'', u'')\
        .replace(u'雷锋网原创文章，未经授权禁止转载。详情见。', '')\
        .replace(u'雷锋网原创文章，未经授权禁止转载。详情见', '')\
        .replace(u'<a href="http://dwz.cn/4ErMxZ" rel="nofollow" target="_blank">转载须知</a>。', u'') \
        .replace(u'转载须知。', u'') \
        .replace(u'转载须知', u'') \
        .replace(u'雷锋网版权文章，未经授权禁止转载。详情见。', u'')\
        .replace(u'雷锋网版权文章，未经授权禁止转载。详情见', u'')

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