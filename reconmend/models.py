# coding=utf-8
from google.appengine.ext import db

	
#推荐文章链接
class Reconmend(db.Model):
	id = db.IntegerProperty()
	url = db.URLProperty()