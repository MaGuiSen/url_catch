# -*- coding: utf-8 -*-
from scrapy import Selector

from util import CssUtil
from util import EncryptUtil
from util import DateUtil
from util.StyleCache import getStyle


def downLoadCss(styleUrls):
    styleList = []
    css = {}
    for styleUrl in styleUrls:
        # 得到hash作为key
        if styleUrl.startswith(u'//'):
            styleUrl = u'http:' + styleUrl
        styleUrlHash = EncryptUtil.md5(styleUrl)
        if styleUrlHash not in css:
            # 不存在则去下载 并保存
            styles = getStyle(styleUrl)
            if styles:
                css[styleUrlHash] = styles
        if css.get(styleUrlHash):
            styleList.append(css.get(styleUrlHash))
    return styleList

def parse(html):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@id="Cnt-Main-Article-QQ"]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") and not(name(.)="style")  and not(name(.)="iframe")'
                                       u'and not(boolean(@class="rv-root-v2 rv-js-root"))] |text()')
    if not content_items:
        return None

    # 处理时间
    post_date = response.xpath(
        u'//*[@class="a_time"]/text() | //*[boolean(contains(@class, "pubTime"))]/text()').extract_first(u'')

    post_date = post_date.replace(u'\xa0', u' ')
    post_date = DateUtil.dateFormat(dateStr=post_date)

    title = response.xpath(u'//*[@class="qq_article"]/div[@class="hd"]/h1/text() |'
                           u' //div[@class="LEFT"]/h1/text() | //title/text()').extract_first(u'')

    content_html = u"""<div id="Cnt-Main-Article-QQ" class="Cnt-Main-Article-QQ" bosszone="content">
                                    %s
                               </div>
                           """ % (u''.join(content_items.extract()),)

    style_in_list = []
    style_need_replace = [
        {u'old': u'width:660px;', u'new': u''},
        {u'old': u'width:660px', u'new': u''},
        {u'old': u'width:930px;', u'new': u''},
        {u'old': u'width:930px', u'new': u''},
        {u'old': u'width:770px;', u'new': u''},
        {u'old': u'width:770px', u'new': u''},
    ]

    content_item = {
        u'title': title,
        u'content_html': content_html,
        u'post_date': post_date,
        u'style_in_list': style_in_list,
        u'style_need_replace': style_need_replace
    }
    return content_item


if __name__ == '__main__':
    pass