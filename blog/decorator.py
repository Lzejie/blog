# coding=utf8

from functools import wraps

from models import Tags

def tags_taker(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        tags_list = Tags.objects.all()
        return fun(tags_cloud=tags_list, *args, **kwargs)
    return wrapper

