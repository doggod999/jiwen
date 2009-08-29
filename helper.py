from google.appengine.ext import db

from models import Article

def article_save(article):
    id = 0
    try:
        aritcles = Article.all().order('-id')
        id = aritcles[0].id + 1
    except:
        id = 1
    article.id = id
    article.put()