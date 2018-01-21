# coding=utf8

from datetime import datetime

from bson import ObjectId
from flask import render_template, request, abort, redirect

from blog import app
from config import ARTICLETYPE
from models import Article, Tags, Comment
from utils import markdown2html, load_content

@app.errorhandler(404)
def page_not_found(error):
    return 'error'
    title = unicode(error)
    message = error.description
    return render_template('errors.html',
                           title=title,
                           message=message)

@app.errorhandler(500)
def internal_server_error(error):
    return 'error'
    title = unicode(error)
    message = error.description
    return render_template('errors.html',
                           title=title,
                           message=message)

@app.route('/')
@app.route('/main')
def index():
    # 获取所有标签
    tags = Tags.objects.all()

    # 获取文章
    now_page_num = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))
    articles = Article.objects[limit*(now_page_num-1):limit*(now_page_num)]
    total_page = Article.objects.count() / limit

    data = {
        'articles':articles,
        'tags_cloud': tags,
        'total_page': total_page+1 if total_page else None,
        'now_page_num': now_page_num,
        'pre_page': '/main?page=%s'%(now_page_num-1),
        'next_page': '/main?page=%s'%(now_page_num+1)
    }

    return render_template('index.html', **data)


@app.route('/tag/<name>')
def show_tag(name):
    # 获取所有标签
    tags = Tags.objects.all()

    now_page_num = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    tag = Tags.objects(name=name).first()
    articles = Article.objects(tags__in=[tag])[limit * (now_page_num-1):limit * (now_page_num)]

    total_page = len(articles) / limit

    data = {
        'articles': articles,
        'tag': name,
        'tags_cloud': tags,
        'total_page': total_page + 1 if total_page else None,
        'now_page_num': now_page_num,
        'articles_count': Article.objects(tags__in=[tag]).count(),
        'pre_page': '/tag/%s?page=%s' % (name, now_page_num-1),
        'next_page': '/tag/%s?page=%s' % (name, now_page_num+1)
    }
    return render_template('tagsArticle.html', **data)


@app.route('/article/<_id>')
def get_article(_id):
    # 获取所有标签
    tags = Tags.objects.all()

    article = Article.objects(id=ObjectId(_id)).first()

    data = {
        'article': article,
        # 'title': article.title,
        # 'content': article.content,
        # 'pub_time': article.createdAt,
        # 'tags': article.tags,
        'tags_cloud': tags
    }
    return render_template('article.html', **data)


@app.route('/about')
def about():
    # 获取所有标签
    tags = Tags.objects.all()
    # 标题
    article = Article.objects(title=u'关于我').first()
    data = {
        'tags_cloud': tags,
        'title': article.title,
        'content': article.content,
        'pub_time': article.createdAt,
        'tags': article.tags
    }
    return render_template('article.html', **data)

@app.route('/comment', methods=['POST'])
def comment():
    if request.method != 'POST':
        return u'访问错误', 404

    article_id = request.form.get('article_id')
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not article_id:
        return u'请指定一篇文章', 400
    if not name:
        return u'请输入用户名', 400
    if not content:
        return u'请输入评论内容', 400

    comment = Comment()
    comment.name = name
    if email:
        comment.email = email
    comment.comment = content

    article = Article.objects(id=article_id).first()
    article.comments.append(comment)

    article.save()
    return redirect('/')


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    # 获取所有标签
    tags = Tags.objects.all()
    # 标题
    article = Article.objects(title=u'关于我').first()
    data = {
        'tags_list': tags,
        'type_list': ARTICLETYPE
    }
    return render_template('publish.html', **data)

@app.route('/add_tag')
def add_tag():
    # TODO: 添加标签的接口，还有界面也没做
    pass


if __name__ == '__main__':
    app.run(debug=True)