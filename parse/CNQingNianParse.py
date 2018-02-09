# -*- coding: utf-8 -*-
from scrapy import Selector
# 中国青年网 详情解析


def parse(html, source_url=u''):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@class="TRS_Editor"]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return None

    # 处理时间
    post_date = u''

    # 处理作者
    post_user = u''

    # 处理来源
    src_ref = response.xpath(u'//span[@id="source_baidu"]/a/text()').extract_first(u'')
    if not src_ref:
        src_ref = response.xpath(u'//span[@id="source_baidu"]//text()').extract()
        src_ref = u''.join(u''.join(src_ref).split())
        if u'来源：' in src_ref:
            src_ref = src_ref.replace(u'来源：', '')
        else:
            src_ref = u''
    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div class="TRS_Editor ">
                            %s
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
    a = u'http://news.youth.cn/kj/201801/t20180116_11291009.htm'
    print a.rindex(u'/')
    print a[0: a.rindex(u'/')]