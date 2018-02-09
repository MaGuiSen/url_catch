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

    fm_list = (
        u'%s/%s/%s' % (month, day, year),
        u'%s-%s-%s' % (year, month, day),
        u'%s/%s/%s' % (year, month, day),
        u'%s\.%s\.%s' % (year, month, day),
        u'%s年%s月%s日\\s+%s:%s' % (year, month, day, hour, minute),
        u'%s/%s/%s\\s+%s:%s' % (year, month, day, hour, minute),
        u'%s-%s-%s\\s+%s:%s' % (year, month, day, hour, minute),
        u'%s/%s/%s\\s+%s:%s:%s' % (month, day, year, hour, minute, second),
        u'%s-%s-%s\\s+%s:%s:%s' % (year, month, day, hour, minute, second),
        u'%s/%s/%s\\s+%s:%s:%s' % (year, month, day, hour, minute, second),
        u'%s\.%s\.%s\\s+%s:%s:%s' % (year, month, day, hour, minute, second),
        u'%s年%s月%s日\\s+%s:%s:%s' % (year, month, day, hour, minute, second)
    )
    key_list = []
    for index in range(0, len(fm_list)):
        key_list.append(u'%s')
    pattern = re.compile((u'(%s)' % u'|'.join(key_list)) % fm_list)

    return re.findall(pattern, content)


if __name__ == '__main__':
    result = findTimeStr(u'高江虹 　2018年01月17日 10:09')
    print result and result[0]