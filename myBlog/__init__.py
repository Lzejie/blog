#coding=utf8

from flask import Flask
from abc import ABCMeta, abstractmethod
from bson import ObjectId
from datetime import datetime

from pymongo import MongoClient

from config import MONGO_EXPRESSION
from config import DBNAME
# from myBlog import utils
# from myBlog import views

# app = Flask(__name__)
# app.config.from_object('config')

class BaseObject(object):
    __metaclass__ = ABCMeta

    def __init__(self, collection, key_list):
        assert isinstance(collection, str) or isinstance(collection, unicode), \
            u'collection必须为一个字符串'.encode('utf8')
        assert isinstance(key_list, list), u'key_list必须为一个列表'
        self.collection = MongoClient(MONGO_EXPRESSION)[DBNAME][collection]
        self.obj = {}
        self.key_list = key_list

    # 创建标签
    def insert(self):
        assert not isinstance(self.obj.get('_id'), ObjectId), u'已存在，请勿重新创建'.encode('utf8')
        for key in self.key_list:
            assert key in self.obj, u'缺少%s'.encode('utf8')%key

        self.obj.update({
            'createdAt': datetime.now(),
            'updatedAt': datetime.now()
        })
        self.obj['_id'] = self.collection.insert(self.obj)

    # 更新标签
    def update(self):
        for key in self.key_list:
            assert key in self.obj, u'缺少%s'.encode('utf8')%key
        assert isinstance(self.obj.get('_id', None), ObjectId), u'该模型未被创建'.encode('utf8')

        self.obj.update({'updatedAt':datetime.now()})

        try:
            self.collection.update_one({'_id': self.obj['_id']}, {'$set': self.obj})
        except Exception,e:
            raise u'更新数据出错 \n %s'.encode('utf8')%str(e)

    # 更新入口
    def edit(self, **kwargs):
        for key in kwargs.keys():
            if key in self.key_list:
                self.obj[key] = kwargs[key]
        self.update()

