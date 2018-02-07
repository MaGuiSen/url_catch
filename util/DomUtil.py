# -*- coding: utf-8 -*-
from scrapy import Selector


def clearAltTitleHref(content_html):
    # 去除 image 的 alt title
    selector = Selector(text=content_html)
    imgAltTitles = selector.xpath(u'//img/@alt|//img/@title').extract()
    # 处理提示块img的 alt title, 关注//img/@alt|//img/@title
    for imgAltTitle in imgAltTitles:
        if imgAltTitle.strip():
            img_alt1 = u'alt="%s"' % imgAltTitle
            img_alt2 = u"alt='%s'" % imgAltTitle
            img_title1 = u'title="%s"' % imgAltTitle
            img_title2 = u"title='%s'" % imgAltTitle
            content_html = content_html.replace(img_alt1, u'').replace(img_alt2, u'')
            content_html = content_html.replace(img_title1, u'').replace(img_title2, u'')

    hrefs = selector.xpath(u'//a/@href').extract()
    for href in hrefs:
        if href.strip():
            a_href1 = u'href="%s"' % href
            a_href2 = u"href='%s'" % href
            content_html = content_html.replace(a_href1, u'').replace(a_href2, u'')
    return content_html


def clearDOM(content_html, clearPaths):
    # 去除 image 的 alt title
    selector = Selector(text=content_html)
    # 去除不要的标签内容
    for path in clearPaths:
        blocks = selector.xpath(path).extract()
        for block in blocks:
            content_html = content_html.replace(block, '')
    return content_html