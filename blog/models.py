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
    comment = StringField(required=True, max_length=1000, min_length=1)
    # email
    email = EmailField()

    request_data = DictField()
    createdAt = DateTimeField(default=datetime.now())

# 文章类
class Article(Document):
    title = StringField(max_length=50)
    summery = StringField(max_length=300, help_text=u'summery')
    content = StringField()
    # 限定选择范围
    article_type = StringField(required=True, choices=ARTICLETYPE)
    # DENY 模式表示在Tag被删除时，如果该tag有关联的文本，则会报错，禁止该次删除操作
    tags = ListField(ReferenceField(Tags, reverse_delete_rule=DENY))
    # 用来放评论
    comments = ListField(EmbeddedDocumentField(Comment))
    # image_list = ListField(ReferenceField(Image))
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField(default=datetime.now())

if __name__ == '__main__':
    # t = Tags.objects.first()
    # print t.name
    # tag = Tags()
    # tag.name = u'关于我'
    # tag.save()

    # article = Article()
    # article.title = u'关于我'
    # article.content = u'<p>学而不思则罔，思而不学则怠</p>'*10
    # article.article_type = u'关于我'
    # article.tags = [Tags.objects(name=u'关于我').first()]
    # article.save()

    tag1 = Tags()
    tag2 = Tags()

    tag1.name = u'test1'
    tag2.name = u'test2'
    tag1.save()
    tag2.save()
    for index in range(10):
        article = Article()

        article.title = 'this is a test%s'%index
        article.summery = 'summery '
        article.content = 'test and this is content'
        article.article_type = u'技术分享'
        article.comments = []
        # tag_id = tag.save()

        tag1 = Tags.objects(name='test1').first()
        tag2 = Tags.objects(name='test2').first()
        article.tags = [tag1, tag2]
        # article.tags.append(tag2)
        article.save()

    