# -*- coding: utf-8 -*-
from scrapy import Selector
# 第一财经详情parse


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@class="m-text"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(
        u'*[not(name(.)="script") and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = u''

    # 处理作者
    post_user = u''

    # 处理来源
    src_ref = response.xpath(u'//*[@class="m-title f-pr"]/h2[@class="f-ff1 f-fwn f-fs14"]/i//text()').extract_first(u'')

    # 处理tags
    tags = response.xpath(u'//meta[@name="keywords"]/@content').extract_first(u'')

    # 组装新的内容标签
    content_html = u"""<div class="m-text">
                         %s
                       </div>
                   """ % (u''.join(content_items.extract()),)

    # 去除不要的标签内容
    clear_paths_in = [u'//script', u'//*[@data-sudaclick="suda_1028_guba"]', u'//*[@id="finance_lcsds_ds_cls"]',
                      u'//*[@class="hqimg_related"]']
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
