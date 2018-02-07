# -*- coding: utf-8 -*-
from readability import Document

from util.DateUtil import findTimeStr
from util.DomUtil import clearDOM


def parse(html):
    doc = Document(html)
    title = doc.title()
    if title == u'[no-title]':
        title = u''
    content_html = doc.summary()
    content_html = content_html.replace(u'<html>', u'').replace(u'</html>', u'')\
        .replace(u'<body>', u'').replace(u'</body>', u'')

    clear_paths = [u'//script', u'//img', u'//a']
    body = clearDOM(html, clear_paths)

    match_list = findTimeStr(body)
    post_date = u''
    for match_item in match_list:
        if len(match_item) > len(post_date):
            post_date = match_item
    print post_date

    style_in_list = []
    style_need_replace = []

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