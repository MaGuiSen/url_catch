# -*- coding: utf-8 -*-
from scrapy import Selector
from util import CssUtil
# 快科技 详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@class="news_info"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@class="jcuo1") '
                                       u' and not(@id="weixin") '
                                       u' and not(@class="news_bq") '
                                       u' and not(@style="width:468px; height:60px;margin:auto; padding:0 0 10px 0") '
                                       u' and not(@style="width:468px; height:60px;margin:auto; padding:15px 0 0 0") '
                                       u' and not(name(.)="table") '
                                       u' and not(@class="btnPrev") '
                                       u' and not(@class="btnNext") '
                                       u' and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    date = response.xpath(u'//div[@class="news_bt1_left"]/text()').extract_first(u'')
    date = date.split()
    post_date = u''
    if len(date):
        post_date = date[0]
        if len(date)>1:
            post_date += (u' ' + date[1])

    # 处理作者
    post_user = u''

    # 处理来源
    src_ref = u'快科技'

    # 处理tags
    tags = response.xpath(u'//span[@class="news_bq_list"]/a/text()').extract()
    tags = u','.join(tags)

    # 组装新的内容标签
    content_html = u"""<div class="news_info">
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