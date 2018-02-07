# -*- coding: utf-8 -*-

style = """

    body {
        min-width: 800px !important;;
        margin: 0;
    }

    .digest {
        background: #ffff00
    }

    .detail-html table {
        margin: 0 auto;
    }
    .detail-html p {
        line-height: 2em;
        margin: 15px 0;
        padding:  0 20pxi;
	text-indent: 28px;
    }
    .detail-html img{
        max-width: 100%;
        margin: 0 auto;
        display: block;
    }
    .detail-html iframe{
        display: none;
    }
    .detail-html ul{
        padding: 0;
        list-style-type: none;
    }

"""


def getCommonStyle():
    return style


if __name__ == '__main__':
    pass
