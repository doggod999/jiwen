# coding=utf-8
from google.appengine.ext import db

class Article(db.Model):
	id = db.IntegerProperty()
	title = db.StringProperty()
	content = db.TextProperty()
	post_time = db.DateTimeProperty(auto_now_add=True)
	last_modify_time = db.DateTimeProperty(auto_now=True)
	author = db.UserProperty(auto_current_user=True)
	read_count = db.IntegerProperty(required=True, default=0)
	category = db.StringProperty()
	from_url = db.URLProperty()
	recommend = db.BooleanProperty(required=True, default=False)
	
class Meta(db.Model):
	id = db.IntegerProperty()
	keys = db.StringProperty()
	description = db.TextProperty()
