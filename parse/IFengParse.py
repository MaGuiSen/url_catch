# -*- coding: utf-8 -*-
from scrapy import Selector

from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)

    # 处理内容区
    content_html = response.xpath(u'//div[@id="main_content"]')
    if not content_html:
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(
        u'*[not(name(.)="script") and not(name(.)="style") and not(name(.)="iframe")]|text()')
    if not content_items:
        return

    # 处理时间
    post_date = response.xpath(u'//meta[contains(@name, "og:time")]/@content').extract_first(u'')
    post_date = post_date.replace(u'\xa0', u' ')

    # 处理作者
    post_user = u''

    # 处理来源
    src_ref = response.xpath(u'//span[@class="ss03"]//text()').extract_first(u'')
    if not src_ref.replace(u'\n', u'').replace(u' ', u''):
        src_ref = response.xpath(u'//div[@id="artical_sth"]/p/text()').extract()
        src_ref = u''.join(src_ref).replace(u'\n', u'').replace(u'来源：', u'').replace(u' ', u'')

    if not src_ref:
        src_ref = response.xpath(u'//div[@id="artical_sth"]/p/span[2]//text()').extract_first(u'')

    # 处理tags
    tags = response.xpath(u'//meta[@name="keywords"]/@content').extract_first('')

    # 组装新的内容标签
    content_html = u"""<div id="artical_real" class="js_img_share_area">
                        <div id="main_content" class="js_selection_area" bosszone="content">
                             %s
                        </div>
                      </div>
                   """ % (u''.join(content_items.extract()),)
    # 去除Logo
    logoHtml = response.xpath(u'//span[@class="ifengLogo"]').extract_first(u'')
    content_html = content_html.replace(logoHtml, u'')

    # 去除不要的标签内容
    clear_paths_in = []
    style_in_list = []
    style_need_replace = [
        {u'old': u'width:600px;', u'new': u''},
        {u'old': u'width:600px', u'new': u''},
        {u'old': u'#eaeaea', u'new': u'#ffffff'}
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
