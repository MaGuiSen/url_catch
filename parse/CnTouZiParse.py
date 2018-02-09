# -*- coding: utf-8 -*-
from scrapy import Selector
from util import CssUtil
# 中国投资咨询网 详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@id="ncontent"]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return None

    date_srf = response.xpath(u'//div[@class="newsinfo"]/div[@class="date"]/span[@class="blue"]/text()').extract()

    src_ref = u''
    post_date = u''
    if len(date_srf):
        src_ref = date_srf[0]
        src_ref = src_ref.replace(u'来源：', u'')
        if len(date_srf) > 1:
            post_date = date_srf[1]

    # 处理时间
    post_date = post_date.replace(u'\xa0', u' ')

    # 处理作者
    post_user = u''

    # 处理tags
    tags = response.xpath(u'//meta[@name="Keywords"]/@content').extract_first('')
    tags = tags.replace(u' ', u',')

    # 组装新的内容标签
    content_html = u"""<div id="class="newsinfo">
                        <div class="cont">
                             %s
                        </div>
                      </div>
                   """ % (u''.join(content_items.extract()),)

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