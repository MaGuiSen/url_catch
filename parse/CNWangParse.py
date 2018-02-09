# -*- coding: utf-8 -*-
from scrapy import Selector
# 中国网详情解析
from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@id="fontzoom"]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u'and not(@class="fr bianj")'
                                       u'and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return None

    date_srf_user = response.xpath(u'//span[@class="fl time2"]//text()').extract()
    date_srf_user = u''.join(date_srf_user).split()

    post_date = u''
    src_ref = u''
    post_user = u''
    if len(date_srf_user) >= 1:
        post_date = date_srf_user[0]
        if len(date_srf_user) >= 2:
            src_ref = date_srf_user[1]
            if len(date_srf_user) >= 3:
                post_user = date_srf_user[2]
                if len(date_srf_user) >= 4:
                    post_user += (u' ' + date_srf_user[3])
                post_user = post_user.replace(u'作者：', '')

    # 处理tags
    tags = u''

    # 得到纯文本，处理来源和作者
    for item in content_items:
        # 文本
        allTxt = item.xpath(u'.//text()').extract()
        allTxt = u''.join(allTxt).replace(u'\t', u'')
        if u'来源：' in allTxt or u'来源:' in allTxt and len(allTxt) < 25:
            # 说明这是真正的来源
            src_ref = allTxt.replace(u'来源：', u'').replace(u'来源:', u'').strip(u' ')
            src_ref = u''.join(src_ref.split())

    # 组装新的内容标签
    content_html = u"""<div id="fontzoom">
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