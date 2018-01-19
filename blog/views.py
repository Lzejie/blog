# coding=utf8

from datetime import datetime
from flask import render_template, request, abort

from blog import app
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
def index():
    # 获取所有标签
    tags = [each.name for each in Tags.objects.all()]

    # 获取文章
    page_num = int(request.args.get('page', 0))
    limit = int(request.args.get('limit', 5))
    articles = Article.objects[limit*page_num:limit*(page_num+1)]
    total_page = Article.objects.count() / limit

    data = {
        'articles':[
            {
                'title': each.title,
                'summery': each.summery,
                'pub_time': each.createdAt,
                'tags': [item.name for item in each.tags],
                # 'author': each.author
            }for each in articles
        ],
        'tags_cloud': tags,
        'total_page': total_page+1,
        'now_page_num': page_num+1
    }

    return render_template('index.html', **data)

@app.route('/article/<_id>')
def get_article(_id):
    # article = Article.objects('_id'==_id)
    data = {
        'title': u'测试',
        'content': u'<p>文章内容测试</p>'*20,
        'pub_time': str(datetime.now().today()),
        'tags': u'测试',
        'author': u'Mr.Foo',
        'tags_cloud': ['tag%s'%index for index in range(1,10)]
    }
    return render_template('article.html', **data)

@app.route('/tag/<name>')
def show_tag(name):
    # 获取所有标签
    tags = Tags.objects.all()

    page_num = int(request.args.get('page', 0))
    limit = int(request.args.get('limit', 5))
    total_page = Article.objects.count() / limit

    tag = Tags.objects(name=name).first()
    articles = Article.objects(tags__in=[tag])[limit * page_num:limit * (page_num + 1)]
    data = {
        'articles': [
            {
                'title': each.title,
                'summery': each.summery,
                'pub_time': each.createdAt,
                'tags': [item.name for item in each.tags],
                # 'author': each.author
            } for each in articles
            ],
        'tags_cloud': tags,
        'total_page': total_page + 1,
        'now_page_num': page_num + 1
    }
    return render_template('tagsArticle.html', **data)

@app.route('/about')
def about():
    # content = load_content('about')
    # return render_template('page.html',
    #                        title='About',
    #                        content=content)
    pass

@app.route('/links')
def links():
    content = load_content('links')
    return render_template('page.html',
                           title='Links',
                           content=content)

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    # if request.method == 'GET':
    #     abort(404)
    #
    # # authorization
    # token = request.form.get('token', '')
    # if token != app.config['TOKEN']:
    #     return 'invalid access token', 500
    #
    # title = request.form.get('title', None)
    # if not title:
    #     return 'no title found', 500
    #
    # summary = request.form.get('summary', None)
    # if not summary:
    #     return 'no summary found', 500
    #
    # content = request.form.get('content', None)
    # if not content:
    #     return 'no content found', 500
    # content = markdown2html(content)
    #
    # pub_time = request.form.get('pub_time', None)
    # if pub_time:
    #     pub_time = datetime.strptime(pub_time, app.config['TIME_FORMAT'])
    #
    # tags = request.form.getlist('tags')
    #
    # create_article(title, summary, content, pub_time, tags)
    # return '', 200
    pass

@app.route('/publishTag', methods=['GET', 'POST'])
def publishTag():
    # if request.method == 'GET':
    #     abort(404)
    #
    # # authorization
    # token = request.form.get('token', '')
    # if token != app.config['TOKEN']:
    #     return 'invalid access token', 500
    #
    # tagsNam = request.form.get('tag', 'tag')
    # create_tag(tagsNam)
    # return None
    pass

if __name__ == '__main__':
    app.run(debug=True)