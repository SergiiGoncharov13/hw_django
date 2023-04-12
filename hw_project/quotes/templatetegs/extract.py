from bson.objectid import ObjectId

from django import template

from ..utils import get_mongo_db

register = template.Library()


def get_author(_id):
    db = get_mongo_db()
    author = db.authors.find_one({'_id': ObjectId(_id)})
    return author['fullname']


register.filter('author', get_author)
