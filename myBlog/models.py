#coding=utf8

from datetime import datetime
from bson import ObjectId

from pymongo import MongoClient

from myBlog import BaseObject
from config import MONGO_EXPRESSION
from config import SUMMERYLENGTH


class Tag(BaseObject):
    def __init__(self, **kwargs):
        BaseObject.__init__(self, collection='tag', key_list=['name', 'createdBy'])
        # 如果传入的数据有_id的话证明是已经创建的对象
        if not isinstance(kwargs.get('_id', None), ObjectId):
            self.obj.update(kwargs)
            self.insert()


class Article(BaseObject):
    def __init__(self, **kwargs):
        BaseObject.__init__(self, collection='article', key_list=['title', 'content', 'createdBy', 'tags'])
        # 如果传入的数据有_id的话证明是已经创建的对象
        if not isinstance(kwargs.get('_id', None), ObjectId):
            self.obj.update(kwargs)
            self.insert()


