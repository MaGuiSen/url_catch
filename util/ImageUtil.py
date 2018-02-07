# -*- coding: utf-8 -*-
import os

import requests

from util import EncryptUtil
from util import FileUtil
from util import TimerUtil
from util.FileUtil import ImageCompressUtil, UploadUtil

fileUtil = UploadUtil(u'/news/' + u'common_catch' + u'/image/')


def downLoadImage(image_url_sources):
    image_urls = []
    for image_url in image_url_sources:
        file_path = os.path.dirname(os.path.realpath(__file__)) + u'/image'
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        url = image_url.get('url')
        print url
        urlHash = EncryptUtil.md5(url)
        fileName = str(urlHash) + '.jpg'
        detailPath = file_path + '\\' + fileName

        if FileUtil.fileIsExist(detailPath):
            print u'图片已经存在本地:' + url
            image_url_new = {
                'ok': True,
                'x': {
                    'url': url,
                    'path': detailPath,
                    'fileName': fileName
                }
            }
        else:
            try:
                fileResponse = requests.get(url, timeout=10)
                req_code = fileResponse.status_code
                req_msg = fileResponse.reason
                if req_code == 200:
                    open(detailPath, 'wb').write(fileResponse.content)
                    # 判断大小是否大于100kb 压缩到600， 质量为80
                    if len(fileResponse.content) > 100 * 1024:
                        # 目标图片大小
                        dst_w = 600
                        dst_h = 600
                        # 保存的图片质量
                        save_q = 80
                        ImageCompressUtil().resizeImg(
                            ori_img=detailPath,
                            dst_img=detailPath,
                            dst_w=dst_w,
                            dst_h=dst_h,
                            save_q=save_q
                        )
                    image_url_new = {
                        'ok': True,
                        'x': {
                            'url': url,
                            'path': detailPath,
                            'fileName': fileName
                        }
                    }
                    # http://p0.ifengimg.com/pmop/2017/1010/E66C2599CE9403A670AD405F4CCAB271B366D7DC_size415_w1290_h692.png
                    print u'图片成功下载,大小:' + str(len(fileResponse.content) / 1024) + 'kb ' + url
                    print u'最终存储图片,大小:' + str(os.path.getsize(detailPath) / 1024) + 'kb ' + url
                else:
                    print u'下载图片失败:' + url
                    image_url_new = {
                        'ok': False,
                        'x': {
                            'url': url,
                        }
                    }
            except Exception, e:
                print u'下载图片失败:' + url
                image_url_new = {
                    'ok': False,
                    'x': {
                        'url': url,
                    }
                }
        image_urls.append(image_url_new)
        # 空转2s
        TimerUtil.sleep(2)

    result_image_urls = []
    for image_url in image_urls:
        ok = image_url.get('ok', False)
        if ok:
            x = image_url.get('x', {})
            url = x['url']
            path = x['path']
            fileName = x['fileName']
            # 上传照片
            imgUrl = fileUtil.upload(path, fileName)
            if imgUrl:
                result_image_urls.append({
                    'url': url,
                    'image_url': imgUrl
                })
                print imgUrl
            # 删除文件
            delImg(url)
    return result_image_urls


def delImg(url):
    file_path = os.path.dirname(os.path.realpath(__file__)) + u'/image'
    urlHash = EncryptUtil.md5(url)
    file_name = str(urlHash) + '.jpg'
    detailPath = file_path + '\\' + file_name
    try:
        FileUtil.delFile(detailPath)
        print (u'删除图片成功:%s' % detailPath)
    except Exception as e:
        print (u'删除图片失败:%s' % str(e))


if __name__ == '__main__':
    downLoadImage([{
        'url': 'https://mp.weixin.qq.com/debug/wxadoc/dev/image/quickstart/basic/register.png?t=201822'
    }])
