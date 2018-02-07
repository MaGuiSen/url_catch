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
    content_html = response.xpath(u'//*[@id="endText"]')
    outHtml = u"""<div class="post_text" id="endText" style="border-top:1px solid #ddd;" jcid="5611">
                        %s
                        </div>
                   """
    if not content_html:
        content_html = response.xpath(u'//*[@id="content"]')
        outHtml = u"""
                    <div class="wrapper">
                        <div class="article_wrap" style="padding-left:0px;">
                            <div class="article_box" style="width:100%;">
                                <div class="content">
                                     %s
                                </div>
                            </div>
                        </div>
                    </div>
                """

    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(boolean(@class="gg200x300" or @class="ep-source cDGray")) '
                                       u'and not(name(.)="script")]|text()')
    if not content_items:
        return None

    post_date = response.xpath(u'//meta[@property="article:published_time"]/@content').extract_first(u'')
    post_date = post_date.replace(u'T', u' ')
    post_date = post_date[0: post_date.rindex(u'+')]
    post_date = DateUtil.dateFormat(dateStr=post_date)

    title = response.xpath(u'//meta[@property="og:title"]/@content | //title/text()').extract_first(u'')

    content_html = outHtml % (u''.join(content_items.extract()),)

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