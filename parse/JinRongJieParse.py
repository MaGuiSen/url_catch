# -*- coding: utf-8 -*-
from scrapy import Selector

from util import DateUtil


def parse(html, source_url=u''):
    response = Selector(text=html)

    content_html = response.xpath(u'//div[@class="texttit_m1"] | //div[@class="vp-article-cnt"]')
    if not len(content_html):
        return

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u'and not(name(.)="style")  '
                                       u'and not(name(.)="iframe") '
                                       u'and not(@class="kline")] | text()')
    if not len(content_items):
        return

    post_date = response.xpath(u'//div[@class="vp-article-source mt30"]/span[@class="time"]/text() '
                               u'| //p[@class="inftop"]/span[1]/text()[1] '
                               u'| //div[@class="inftop"]//span[@class="time"]/text()[1]').extract_first(u'')

    post_date = post_date.replace(u'\xa0', u' ')

    # 处理标题
    title = response.xpath(u'//div[@class="vp-article"]/h1/text() '
                           u'| //div[@class="titmain"]/h1//text()[3] '
                           u'| //div[@class="texttitbox"]/h1/text()[3]').extract_first(u'')

    # 处理作者
    post_user = u''

    # 处理来源
    src_ref = response.xpath(u'//div[@class="vp-article-source mt30"]/a[@class="name"]/text() '
                             u'| //p[@class="inftop"]/span[2]//text() '
                             u'| //div[@class="inftop"]//span[@class="urladd"]//text()').extract()

    src_ref = ''.join(src_ref).replace(u'来源：', u'')

    # 处理tags
    tags = response.xpath(u'//meta[@name="keywords"]/@content').extract_first(u'')

    # 组装新的内容标签
    content_html = u"""<div class="titimg">
                                    <div class="texttit_m1">
                                       %s
                                    </div>
                                  </div>
                               """ % (u''.join(content_items.extract()),)

    content_html = content_html.replace(u'<strong>（</strong>', '') \
        .replace(u'<strong>）</strong>', '') \
        .replace(u'<p align="center">获取更多精彩内容，欢迎搜索关注</p>', '') \
        .replace(u'下载A，随时关注更多优惠信息', '').replace(u'文章整理自', '')

    # 去除不要的标签内容
    clear_paths_in = [u'//script',
                      u'//a[@style="TEXT-DECORATION: none"]',
                      u'//img[@style="VERTICAL-ALIGN: middle"]/@src',
                      u'//font[@face="Courier"]',
                      u'//a[@href="https://8.jrj.com.cn/ad/promotion/go_new_1888?tgqdcode=3643QR3G&ylbcode=PJV27Y49"]']

    style_in_list = []
    style_need_replace = [
        {u'old': u'background:#efefef;', u'new': u''},
        {u'old': u'background:#efefef', u'new': u''},
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


if __name__ == u'__main__':
    pass
