# -*- coding: utf-8 -*-
from scrapy import Selector
# cnbeta 详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@id="artibody"]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@class="article-topic")'
                                       u' and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return None

    # 处理时间
    post_date = response.xpath(u'//div[@class="meta"]/span[1]/text()').extract_first(u'')

    # 处理作者
    post_user = u''

    # 处理来源
    src_ref = u''.join(response.xpath(u'//div[@class="meta"]/span[@class="source"]//text()').extract())
    src_ref = src_ref.replace(u'稿源：', u'')

    # 处理tags
    tags = u''

    article_summary = response.xpath(u'//div[@class="article-summary"]').extract_first(u'')

    # 组装新的内容标签
    content_html = u"""
                      %s
                      <div class="article-content">
                             %s
                      </div>
                   """ % (article_summary, u''.join(content_items.extract()))

    style_in_list = []
    style_need_replace = []

    title = response.xpath(u'//meta[@property="og:title"]/@content | //title/text()').extract_first(u'')

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