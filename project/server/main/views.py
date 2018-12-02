# project/server/main/views.py


from flask import render_template, Blueprint


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/info')
def home():
    return '测试'


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
