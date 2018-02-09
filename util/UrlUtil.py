# -*- coding: utf-8 -*-
import urlparse


def getNetLoc(url):
    result = urlparse.urlsplit(url)
    return u'http://' + result.netloc


if __name__ == '__main__':
    pass