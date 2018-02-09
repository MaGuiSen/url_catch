# -*- coding: utf-8 -*-
from scrapy import Selector


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@id="first"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@style="display:none;")'
                                       u' and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//*[@class="p_tatime"]/text()').extract_first(u'').replace(u'\xa0', u' ')

    # 处理作者
    post_user = response.xpath(u'//*[@style="color:black;display:inline-block;padding:0 5px;"]/text()').extract()

    # 处理来源
    src_ref = u'淘股吧'

    # 处理tags
    tags = response.xpath(u'//*[starts-with(@href,"Keyword/")]/text()').extract()
    tags = u','.join(tags)

    # 组装新的内容标签
    content_html = u"""<div class="article-cont">
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
            img_str_new = img_str_old.replace(u'data-original', u'src')
        else:
            img_src_new = img.xpath(u'@data-original').extract_first('')
            img_str_new = img_str_old.replace(img_src_old, img_src_new)
        content_html = content_html.replace(img_str_old, img_str_new)

    # 去除不要的标签内容
    clear_paths_in = []
    style_in_list = []
    style_need_replace = [{
        {u'old': u'#f2f4f2', u'new': u'#f2f4f2'},
    }]

    title = response.xpath(u'//meta[@property="og:title"]/@content | //title/text()').extract_first(u'')

    content_item = {
        u'title': title,
        u'content_html': content_html,
        u'post_date': post_date,
        u'style_in_list': style_in_list,
        u'style_need_replace': style_need_replace,
        u'clear_paths_in': clear_paths_in,
    }

    return content_item


if __name__ == '__main__':
    pass