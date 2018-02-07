# -*- coding: utf-8 -*-
import re
import time


def dateFormat(dateStr='', targetFormat=''):
    if not dateStr:
        return ''
    dateStr = dateStr \
        .replace('\r\n', '') \
        .replace('\n', '') \
        .strip(' ') \
        .replace(u'年', '-') \
        .replace(u'月', '-') \
        .replace(u'日', ' ')
    needFormats = [
        u'%Y-%m-%d',
        u'%Y/%m/%d',
        u'%m/%d/%Y',
        u'%Y.%m.%d',
        u'%m/%d/%Y %H:%M:%S',
        u'%Y-%m-%d %H:%M',
        u'%Y-%m-%d %H:%M:%S',
        u'%Y/%m/%d %H:%M',
        u'%Y/%m/%d %H:%M:%S',
        u'%Y.%m.%d %H:%M:%S'
    ]
    targetFormat = targetFormat or u'%Y-%m-%d %H:%M:%S'
    for needFormat in needFormats:
        try:
            result = time.strftime(targetFormat, time.strptime(dateStr, needFormat))
            # self.logInfo(u'匹配时间成功：' + result)
            return result
        except Exception as e:
            continue
    print u'未匹配时间：' + dateStr
    return ''


def findTimeStr(content):
    year = u'\d{4}'
    month = u'\d?\d{1}'
    day = u'\d?\d{1}'
    hour = u'\d?\d{1}'
    minute = u'\d?\d{1}'
    second = u'\d?\d{1}'

    fm_1 = u'%s/%s/%s' % (month, day, year)
    fm_2 = u'%s-%s-%s' % (year, month, day)
    fm_3 = u'%s/%s/%s' % (year, month, day)
    fm_4 = u'%s\.%s\.%s' % (year, month, day)
    fm_5 = u'%s/%s/%s\\s+%s:%s' % (year, month, day, hour, minute)
    fm_6 = u'%s-%s-%s\\s+%s:%s' % (year, month, day, hour, minute)
    fm_7 = u'%s/%s/%s\\s+%s:%s:%s' % (month, day, year, hour, minute, second)
    fm_8 = u'%s-%s-%s\\s+%s:%s:%s' % (year, month, day, hour, minute, second)
    fm_9 = u'%s/%s/%s\\s+%s:%s:%s' % (year, month, day, hour, minute, second)
    fm_10 = u'%s\.%s\.%s\\s+%s:%s:%s' % (year, month, day, hour, minute, second)

    pattern = re.compile(
        u'(%s|%s|%s|%s|%s|%s|%s|%s|%s|%s)' % (fm_10, fm_9, fm_8, fm_7, fm_6, fm_5, fm_4, fm_3, fm_2, fm_1))

    return re.findall(pattern, content)