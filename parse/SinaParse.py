# -*- coding: utf-8 -*-
from scrapy import Selector

from util.StyleCache import getStyle
from util.DateUtil import dateFormat
from util import CssUtil
from util import EncryptUtil


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
    content_html = response.xpath(u'//*[@id="artibody"][1] | //*[@id="article"][1]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(boolean(@class="entHdPic")) '
                                       u'and not(@class="content-page") '
                                       u'and not(@class="article-editor") '
                                       u'and not(@class="ct_hqimg") '
                                       u'and not(@id="left_hzh_ad") '
                                       u'and not(name(.)="style") '
                                       u'and not(name(.)="iframe") '
                                       u'and not(name(.)="script")]|text()')
    if not content_items:
        return None

    # 处理时间
    post_date = response.xpath(
        u'//*[@id="pub_date"]/text() | //*[@class="titer"]/text() | //*[@class="date-source"]'
        u'/span[@class="date"]/text() | //meta[@name="weibo: article:create_at"]/@content') \
        .extract_first(u'')
    post_date = dateFormat(dateStr=post_date)

    title = response.xpath(u'//*[@id="artibodyTitle"]/text() | //*[@id="main_title"]/text() | '
                           u'//meta[@property="og:title"]/@content').extract_first(u'')

    # 组装新的内容标签
    content_html = u"""<div class="content_wrappr_left article article_16 article-content-left">
                           <div class="content">
                             <div class="BSHARE_POP blkContainerSblkCon clearfix blkContainerSblkCon_16" id="artibody">
                                %s
                             </div>
                           </div>
                         </div>
                      """ % (u''.join(content_items.extract()),)

    style_in_list = response.xpath(u'//style/text()').extract()
    style_need_replace = [
        {u'old': u'overflow-x:hidden', u'new': u''},
        {u'old': u'overflow:hidden', u'new': u''},
        {u'old': u'width:680px;', u'new': u''},
        {u'old': u'width:680px', u'new': u''},
        {u'old': u'width:640px;', u'new': u''},
        {u'old': u'width:640px', u'new': u''},
        {u'old': u'width:880px;', u'new': u''},
        {u'old': u'width:880px', u'new': u''},
        {u'old': u'width:850px;', u'new': u''},
        {u'old': u'width:850px', u'new': u''},
    ]
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
