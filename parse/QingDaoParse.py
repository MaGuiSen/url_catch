# -*- coding: utf-8 -*-
from scrapy import Selector


# 青岛 详情解析


def parse(html, source_url=u''):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@class="content"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@class="clear")'
                                       u' and not(@class="shang")'
                                       u' and not(name(.)="style") '
                                       u' and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//meta[@property="og:release_date"]/@content').extract_first(u'')

    srf_user = response.xpath(u'//div[@class="resource1000"]//text()')
    srf_user = u''.join(srf_user.extract()).split()

    post_user = u''
    src_ref = u''
    if len(srf_user) and u'来源' in srf_user[0]:
        src_ref = srf_user[0].replace(u'来源：', u'')
    if len(srf_user) > 1 and u'作者' in srf_user[1]:
        post_user = srf_user[1].replace(u'作者：', u'')

    # 处理tags
    tags = u''

    # 组装新的内容标签
    content_html = u"""<div class="content">
                             %s
                      </div>
                   """ % (u''.join(content_items.extract()),)

    selector = Selector(text=content_html)
    # 解析文档中的所有图片url，然后替换成标识
    imgs = selector.xpath(u'descendant::img')
    for img in imgs:
        img_str_old = img.extract()
        img_src_old = img.xpath(u'@src').extract_first('')
        if not img_src_old:
            img_str_new = img_str_old.replace(u'original', u'src')
        else:
            img_src_new = img.xpath(u'@original').extract_first('')
            img_str_new = img_str_old.replace(img_src_old, img_src_new)
        content_html = content_html.replace(img_str_old, img_str_new)



    # 去除不要的标签内容
    clear_paths_in = []
    style_in_list = []
    style_need_replace = [
        {u'old': u'width:680px;', u'new': u''},
        {u'old': u'width:680px', u'new': u''},
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