# -*- coding: utf-8 -*-
from scrapy import Selector
# ITBear 详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@id="content"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@align="center") '
                                       u' and not(name(.)="style") '
                                       u' and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    date_src_user = response.xpath(u'//div[@class="px14"]/text()').extract_first(u'').split()

    post_date = u''
    src_ref = u''
    post_user = u''

    if len(date_src_user):
        post_date = date_src_user[0].replace(u'发布时间：', u'')
    if len(date_src_user) > 1:
        post_date += (u' ' + date_src_user[1])
    if len(date_src_user) > 2 and date_src_user[2].startswith(u'来源：'):
        src_ref = date_src_user[2].replace(u'来源：', u'')
    if len(date_src_user) > 3 and date_src_user[3].startswith(u'编辑：'):
        post_user = date_src_user[3].replace(u'编辑：', u'')

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div id="content" style="overflow-x: hidden; word-break: break-all;">
                          %s
                      </div>
                   """ % (u''.join(content_items.extract()),)

    content_html = content_html.replace(u'声明：本文仅为传递更多网络信息，不代表ITBear观点和意见，仅供参考了解，更不能作为投资使用依据。', u'')

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
