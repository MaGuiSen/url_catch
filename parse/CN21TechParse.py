# -*- coding: utf-8 -*-
import requests
import scrapy
from scrapy import Selector
from util import CssUtil
# 21CN科技 详情解析
from util import DateUtil


def detailParseNext(url, item_obj):
    response = requests.get(url, timeout=200)
    response.encoding = u'utf-8'
    html = response.text
    selector = Selector(text=html)
    # 处理内容区
    content_html = selector.xpath(u'//div[@id="article_text"]')
    if not content_html:
        return item_obj
    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@id="embed_hzh_div")'
                                       u' and not(@class="page-box")'
                                       u' and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return item_obj

    # 组装新的内容标签
    content_html = u"""<div id="article-cmt">
                            <div class="bd">
                             %s
                            </div>
                      </div>
                   """ % (u''.join(content_items.extract()),)
    item_obj[u'content_html'] += content_html

    # 如果有下一页
    next_page = selector.xpath(u'//div[@class="page-box"]//a')
    if next_page:
        next_page = next_page[-1]
        next_page_title = next_page.xpath(u'./text()').extract_first(u'')
        next_page_url = next_page.xpath(u'./@href').extract_first(u'')
        if next_page_title == u'下一页' and next_page_url:
            base_url = url[0: url.rindex(u'/')] + u'/'
            url = base_url + next_page_url
            item_obj = detailParseNext(url, item_obj)
    return item_obj


def parse(html, source_url=u''):
    response = Selector(text=html)
    # 处理内容区
    content_html = response.xpath(u'//div[@id="article_text"]')
    if not content_html:
        return None

    # 去除内部不需要的标签
    content_items = content_html.xpath(u'*[not(name(.)="script") '
                                       u' and not(@id="embed_hzh_div")'
                                       u' and not(@class="page-box")'
                                       u' and not(name(.)="style")  and not(name(.)="iframe")]|text()')
    if not content_items:
        return None

    # 处理时间
    post_date = response.xpath(u'//span[@class="pubTime"]/text()').extract_first(u'')

    # 处理作者
    post_user = response.xpath(u'//span[@class="infoAuthor"]/text()').extract_first(u'')
    post_user = post_user.replace(u'作者：', u'')

    # 处理来源
    src_ref = response.xpath(u'//a[@rel="nofollow"]/text()').extract_first(u'')

    # 处理tags
    tags = u''

    title = response.xpath(u'//meta[@property="og:title"]/@content | //title/text()').extract_first(u'')

    style_in_list = []
    style_need_replace = []

    # 组装新的内容标签
    content_html = u"""<div id="article-cmt">
                            <div class="bd">
                             %s
                            </div>
                      </div>
                   """ % (u''.join(content_items.extract()),)

    content_item = {
        u'title': title,
        u'content_html': content_html,
        u'post_date': post_date,
        u'style_in_list': style_in_list,
        u'style_need_replace': style_need_replace,
    }

    # 处理下一页逻辑
    # 如果有下一页，记住需要用response，因为前面已经把下一页按钮去除
    next_page = response.xpath(u'//div[@class="page-box"]//a')
    if next_page:
        next_page = next_page[-1]
        next_page_title = next_page.xpath(u'./text()').extract_first(u'')
        next_page_url = next_page.xpath(u'./@href').extract_first(u'')
        if next_page_title == u'下一页' and next_page_url:
            base_url = source_url[0: source_url.rindex(u'/')] + u'/'
            next_page_url = base_url + next_page_url
            content_item = detailParseNext(next_page_url, content_item)

    return content_item


if __name__ == '__main__':
    pass