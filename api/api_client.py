# -*- coding: utf-8 -*-

import sys
from flask import Flask

from api.style import getCommonStyle
from catch.common_catch import catch

sys.path.append('../')

app = Flask(__name__, static_url_path='')
app.static_folder = ''

import json
import logging
import traceback

from flask import request, Response, Blueprint

_logger = logging.getLogger(__name__)

# flask模块对象
hq_sema_etl = Blueprint('hq_sema_etl', __name__)


def construct_response(code, msg=None, data=None):
    """
    构建标准请求返回结果
    :param data: 数据内容
    :param code: 错误编码
    :param msg: 错误信息
    """
    return json.dumps({u'code': code, u'msg': msg, u'data': data})


def base_func(operate_func):
    try:
        # 获取参数
        action_params_kv = {}
        for p in request.args:
            action_params_kv[p] = request.args[p]
            print p, '=', request.args[p]
        params = request.form or []
        for p in params:
            action_params_kv[p] = params[p]
            print p, '=', params[p]
        code, msg, data = operate_func(action_params_kv)
    except Exception as e:
        _logger.error(traceback.format_exc())
        code = 500
        msg = str(e)
        data = None
        print msg
    res_text = construct_response(code, msg, data)
    html = ''
    if data:
        styles = data.get(u'styles', u'')
        title = data.get(u'title', u'')
        post_date = data.get(u'post_date', u'')
        content_html = data.get(u'content_html', u'')
        html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>%s</title>
                <style>%s</style>
            </head>
            <body>
            <div class="detail-html">
            %s
            %s
            </div>
            </body>
            </html>
        """ % (title, getCommonStyle(), post_date, content_html)
    _logger.debug(res_text)
    # return res_text  # Response(res_text, mimetype='applications/json')
    return Response(html, mimetype='text/html')


@hq_sema_etl.route('/common/catch', methods=['GET'])
def com_catch():
    def operate(params_req):
        url = params_req.get(u'url', u'')
        if not url:
            return -100, u'请输入爬取路径'
        return catch(url)

    return base_func(operate)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    app.register_blueprint(hq_sema_etl)
    app.run(debug=False, host='0.0.0.0', port=10012, threaded=True)
