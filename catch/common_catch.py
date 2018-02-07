# -*- coding: utf-8 -*-
import time

from scrapy import Selector
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
# https://pythonscraping.com/pages/javascript/redirectDemo1.html 测试重定向的地址
from parse import CommonParse
from parse import SinaParse
from parse import TengXunParse
from parse import WangYiParse

from from_check import *
from util import CssUtil
from util import EncryptUtil
from util import ImageUtil
from util.DomUtil import clearAltTitleHref, clearDOM
from util.StyleCache import getStyle


def loadPage(url):
    print u'开始加载'

    def wait_for_load(a_driver):
        element = a_driver.find_element_by_tag_name(u'html')
        count = 0
        while True:
            count += 1
            # 超过5s，直接返回,看情况设置
            if count > 5:
                print(u'Timing out after 5s and returning')
                return
            print u'睡眠1s'
            time.sleep(0.5)  # 检查还是不是同一个element，如果不是，说明这个html标签已经不再DOM中了。如果不是抛出异常
            new = a_driver.find_element_by_tag_name(u'html')
            if element != new:
                raise StaleElementReferenceException(u'刚才重定向了！')

    driver = webdriver.PhantomJS()
    driver.get(url)
    try:
        wait_for_load(driver)
    except StaleElementReferenceException as e:
        print e.msg
    finally:
        return driver.current_url, driver.page_source


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


def catch(url):
    curr_url, html = loadPage(url)
    # 解析
    # 判断内容解析方式
    content_item = None
    if is_sina(curr_url):
        content_item = SinaParse.parse(html)
    elif is_tengxun(curr_url):
        content_item = TengXunParse.parse(html)
    elif is_wangyi(curr_url):
        content_item = WangYiParse.parse(html)
    content_item_common = CommonParse.parse(html) or {}
    content_item = content_item or {}
    title = content_item.get(u'title') or content_item_common.get(u'title') or u''
    post_date = content_item.get(u'post_date') or content_item_common.get(u'post_date') or u''
    content_html = content_item.get(u'content_html') or content_item_common.get(u'content_html') or u''
    if not title and not post_date and not content_html:
        return -100, u'没有抓取到相关内容', None
    else:
        # 得到最终的结果
        styles = u''
        if content_html:
            # 才去得到styles,和图片
            # 这里得到样式 TODO..暂时不写
            # style_in_list = content_item.get(u'style_in_list') or content_item_common.get(u'style_in_list') or []
            # response = Selector(text=html)
            # styleUrls = response.xpath(u'//link[@rel="stylesheet"]/@href').extract()
            # styleList = downLoadCss(styleUrls + style_in_list)
            # styles = CssUtil.compressCss(styleList).replace(u'\'', u'"').replace(u'\\', u'\\\\')
            # styles = CssUtil.clearUrl(styles)
            # style_need_replace = content_item.get(u'style_need_replace') or content_item_common.get(
            #     u'style_need_replace') or []
            # for replace_item in style_need_replace:
            #     old = replace_item.get(u'old', u'')
            #     new = replace_item.get(u'new', u'')
            #     styles = styles.replace(old, new)

            # 处理图片
            selector = Selector(text=content_html)
            # 解析文档中的所有图片url，然后替换成标识
            image_urls = []
            imgs = selector.xpath(u'descendant::img')

            for img in imgs:
                # 图片可能放在src 或者data-src
                image_url_base = img.xpath(u'@src').extract_first('')
                if image_url_base.startswith(u'//'):
                    image_url = u'http:' + image_url_base
                else:
                    image_url = image_url_base
                if image_url and image_url.startswith(u'http'):
                    print (u'得到图片：' + image_url)
                    image_urls.append({
                        u'url': image_url,
                    })
                    content_html = content_html.replace(image_url_base, image_url)

            # TODO..先不下载
            image_urls = []
            result_image_urls = ImageUtil.downLoadImage(image_urls)
            for item in result_image_urls:
                url = item.get(u'url', u'')
                image_url = item.get(u'image_url', u'')
                content_html = content_html.replace(u'&amp;', u'&').replace(url, image_url)

            # 去除 image 的 alt title
            content_html = clearAltTitleHref(content_html)

            # 去除不要的标签内容
            clearPaths = [u'//script']
            content_html = clearDOM(content_html, clearPaths)

        return upload_result(title, post_date, content_html, styles)


# 上传抓取的结果
def upload_result(title, post_date, content_html, styles):
    if u'|' in title:
        title = title[0: title.index(u'|')]
    if u'_' in title:
        title = title[0: title.index(u'_')]
    if u'-' in title:
        title = title[0: title.index(u'-')]
    print title
    print post_date
    print content_html
    print styles
    content_item = {
        u'title': title,
        u'post_date': post_date,
        u'content_html': content_html,
        u'styles': styles
    }
    return 200, u'成功', content_item


def start():
    # url = u'http://www.jiemian.com/article/1932215.html'
    url = u'http://www.jiemian.com/article/1931697.html'
    while True:
        if not url:
            continue
        catch(url)
        url = u''


if __name__ == u'__main__':
    start()
