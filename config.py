#coding=utf8

import os

AUTHOR = 'Hackii'

# this is useful for submitting markdow files
# when publish new articles
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

HOST='localhost'
PORT='27017'
DBNAME = 'test'
MONGO_EXPRESSION = 'mongodb://%s:%s'%(HOST, PORT)

SUMMERYLENGTH = 150

# 大目录
ARTICLETYPE = [u'技术分享', u'个人感悟', u'阅读', u'关于']

