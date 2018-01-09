# -*- coding: utf-8 -*-
# @Time    : 18/1/2 上午9:03
# @Author  : Edward
# @Site    :
# @File    : tmp.py
# @Software: PyCharm Community Edition

import json
import pickle

from flask import Flask
from flask import request
from flask import jsonify

from taker import taker

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/get_list')
@taker
def  get_list():
    data = pickle.load(open('./data.pkl'))
    return data.keys()

@app.route('/get_value')
@taker
def get_value():
    key = request.args.get('k')
    if not key:
        return u'请传入k'.encode('utf8')
    data = pickle.load(open('./data.pkl'))
    return data.get(key, u'你在逗我？？这个k不存在！')

@app.route('/set_value')
@taker
def set_value():
    key = request.args.get('k')
    value = request.args.get('v')
    if not key or not value:
        return u'请传入k 和 v'.encode('utf8')

    data = pickle.load(open('./data.pkl'))
    data[key] = value
    pickle.dump(data, open('./data.pkl', 'w'))

    return u'设置成功'.encode('utf8')

@app.errorhandler(404)
def page_not_found(error):
    return u'<center><h1>傻逼，这个地址没东西</h1></center>'

if __name__ == '__main__':
    app.run(host='0.0.0.0')