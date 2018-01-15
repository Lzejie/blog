# coding=utf8
from datetime import datetime

from mongoengine import *
from config import DBNAME, HOST, PORT, ARTICLETYPE

connect(DBNAME, host=HOST)

# 标签类
class Tags(Document):
    name = StringField(required=True, max_length=20, unique=True)

    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField(default=datetime.now())

# 评论类，不存在一个具体的表
class Comment(EmbeddedDocument):
    name = StringField(required=True, max_length=20)
    comment = StringField(required=True, max_length=1000, min_length=5)
    # email
    email = EmailField()
    # to save the request info, like ip_address, browser , etc.
    request_data = DictField()
    createdAt = StringField(default=datetime.now())

# 文章类
class Article(Document):
    title = StringField(max_length=50)
    summery = StringField(max_length=300, help_text=u'summery')
    content = StringField()
    # 限定选择范围
    article_type = StringField(required=True, choices=ARTICLETYPE)
    # DENY 模式表示在Tag被删除时，如果该tag有关联的文本，则会报错，禁止该次删除操作
    tags = ListField(ReferenceField(Tags, reverse_delete_rule=DENY))
    # image_list = ListField(ReferenceField(Image))
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField(default=datetime.now())

if __name__ == '__main__':
    # t = Tags.objects.first()
    # print t.name
    tag1 = Tags()
    tag2 = Tags()
    article = Article()

    tag1.name = u'test1'
    tag2.name = u'test2'
    tag1.save()
    tag2.save()
    
    article.title = 'this is a test'
    article.summery = 'summery '
    article.content = 'test and this is content'

    # tag_id = tag.save()


    article.tags = [tag1]
    article.tags.append(tag2)
    article.save()

    