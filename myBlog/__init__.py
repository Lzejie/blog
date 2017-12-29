#coding=utf8

from flask import Flask
from abc import ABCMeta, abstractmethod
from bson import ObjectId
from datetime import datetime

from pymongo import MongoClient

from config import MONGO_EXPRESSION
from myBlog import utils
from myBlog import views

app = Flask(__name__)
app.config.from_object('config')

class BaseObject(object):
    __metaclass__ = ABCMeta

    def __init__(self, collection, key_list):
        assert isinstance(collection, str) or isinstance(collection, unicode), \
            u'collection必须为一个字符串'.encode('utf8')
        assert isinstance(key_list, list), u'key_list必须为一个列表'
        self.collection = MongoClient(MONGO_EXPRESSION)[collection]
        self.obj = {}
        self.key_list = key_list

    @abstractmethod
    def create(self):
        pass

    def __insert(self):
        assert not isinstance(self.obj.get('_id'), ObjectId), u'已存在，请勿重新创建'.encode('utf8')
        for key in self.key_list:
            assert key in self.obj, u'缺少%s'.encode('utf8')%key

        self.obj.update({
            'createdAt': datetime.now(),
            'updatedAt': datetime.now()
        })

        self.collection.insert(self.obj)

    def __update(self, _id, update_data):
        for key in self.key_list:
            assert key in self.obj, u'缺少%s'.encode('utf8')%key

        _id = ObjectId(_id) if isinstance(_id, str) or isinstance(_id, unicode) else _id
        self.obj.update({'updatedAt':datetime.now()})

        try:
            self.collection.update_one({'_id': _id}, {'$set': update_data})
        except Exception,e:
            raise u'更新数据出错 \n %s'.encode('utf8')%str(e)
