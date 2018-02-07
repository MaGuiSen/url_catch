# -*- coding: utf-8 -*-
# 分为多个文件，防止出现同时操作文件的问题，以spiderName作为文件名
import json
import os
import shutil

import datetime

from util import CssUtil
from util import EncryptUtil
from util import FileUtil


def getFilePath(url_hash):
    # 判断当前文件是否存在，不存在，则新建
    fileName = url_hash + u'.json'
    filePath = os.path.join(os.path.dirname(__file__) + u'/styles/')

    if not os.path.exists(filePath):
        os.mkdir(filePath)

    return filePath + fileName


def getStyle(url):
    url_hash = EncryptUtil.md5(url)
    # 先检查缓存里面的style
    file_path = getFilePath(url_hash)
    loadF = None
    try:
        if not os.path.exists(file_path):
            # 不存在，则需要下载
            styles = CssUtil.downLoad(url)
            if styles:
                with open(file_path, u'w') as loadF:
                    json.dump({
                        u'update_time': datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S'),
                        u'url': url,
                        u'styles': styles
                    }, loadF)
            return styles
        else:
            with open(file_path, u'r') as loadF:
                detail = json.load(loadF)
                update_time = detail[u'update_time']
                styles = detail[u'styles']
                # 如果更新时间之间相差5天，就下载
                update_time = datetime.datetime.strptime(update_time, u'%Y-%m-%d  %H:%M:%S')
                now = datetime.datetime.now()
                space_day = (now - update_time).days
                if space_day >= 5:
                    # 需要重新下载
                    loadF.close()
                    FileUtil.delFile(file_path)
                    return getStyle(url)
                else:
                    # 不需要重新下载
                    return styles
    finally:
        if loadF:
            loadF.close()


def clearAllStatus():
    filePath = os.path.join(os.path.dirname(__file__) + u'/styles/')
    shutil.rmtree(filePath)
    os.mkdir(filePath)


if __name__ == u'__main__':
    # getStyle(u'http://c.csdnimg.cn/public/common/libs/bootstrap/css/bootstrap.min.css')
    pass