#coding=utf8

# from datetime import datetime
# from bson import ObjectId
#
# from pymongo import MongoClient
#
# from blog import BaseObject
# from config import MONGO_EXPRESSION
# from config import SUMMERYLENGTH
#
#
# class Tag(BaseObject):
#     def __init__(self, **kwargs):
#         BaseObject.__init__(self, collection='tag', key_list=['name', 'createdBy'])
#         # 如果传入的数据有_id的话证明是已经创建的对象
#         if not isinstance(kwargs.get('_id', None), ObjectId):
#             self.obj.update(kwargs)
#             self.insert()
#
#
# class Article(BaseObject):
#     def __init__(self, **kwargs):
#         BaseObject.__init__(self, collection='article', key_list=['title', 'content', 'createdBy', 'tags'])
#         # # 如果传入的数据有_id的话证明是已经创建的对象
#         # if not isinstance(kwargs.get('_id', None), ObjectId):
#         #     self.obj.update(kwargs)
#         #     self.insert()
#         pass
#
#     def load_all_article(self):
#         return

from pymongo import MongoClient

from config import MONGO_EXPRESSION, DBNAME

DB = MongoClient(MONGO_EXPRESSION)[DBNAME]

def load_data(collection_name, sorted_by='updatedAt', order=1, limit_count=10, ret=None):
    collection = DB[collection_name]
    ret_data = []
    if ret:
        ret_data = [item for item in collection.find({}).sort({sorted_by: order}, ret).limit(limit=limit_count)]
    else :
        ret_data = [item for item in collection.find({}).sort({sorted_by: order}).limit(limit=limit_count)]

    return ret_data


