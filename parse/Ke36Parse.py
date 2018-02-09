# -*- coding: utf-8 -*-

from scrapy import Selector


# 36ke详情parse


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//section[@class="textblock"][1]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script")]|text()')
    if not content_items:
        return

    post_date = u''

    # 处理来源
    src_ref = u''

    # 处理tags
    tags = response.xpath(
        u'//section[@class="single-post-tags"]/a/text()').extract() or []
    tags = u','.join(tags)

    # 组装新的内容标签
    content_html = u"""<div class="article-detail">
                        <div class="content-wrapper">
                          <div class="textblock">
                             %s
                          </div>
                        </div>
                      </div>
                   """ % (u''.join(content_items.extract()),)

    content_html = content_html.replace(u'load-html-img', '')

    selector = Selector(text=content_html)
    # 解析文档中的所有图片url，然后替换成标识
    imgs = selector.xpath(u'descendant::img')
    for img in imgs:
        img_str_old = img.extract()
        img_src_old = img.xpath(u'@src').extract_first('')
        if not img_src_old:
            img_str_new = img_str_old.replace(u'data-src', u'src')
        else:
            img_src_new = img.xpath(u'@data-src').extract_first('')
            img_str_new = img_str_old.replace(img_src_old, img_src_new)
        content_html = content_html.replace(img_str_old, img_str_new)

    # 去除不要的标签内容
    clear_paths_in = []
    style_in_list = []
    style_need_replace = [
        {u'old': u'overflow-x:hidden', u'new': u''},
        {u'old': u'overflow:hidden', u'new': u''},
        {u'old': u'padding-bottom:568px;', u'new': u''},
        {u'old': u'padding-bottom:568px', u'new': u''},
        {u'old': u'padding-bottom:371px;', u'new': u''},
        {u'old': u'padding-bottom:371px', u'new': u''}
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