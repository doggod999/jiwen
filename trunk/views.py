#coding=utf-8

from __future__ import division
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.core.paginator import *

from google.appengine.api import users
from google.appengine.ext import db

from models import Article
from models import Meta
import static

def article_save(article):
    id = 0
    try:
        aritcles = Article.all().order('-id')
        id = aritcles[0].id + 1
    except:
        id = 1
    article.id = id
    article.put()
    return id

def index(request):
	articles_newest = db.GqlQuery("SELECT * FROM Article ORDER BY id DESC").fetch(10)
	articles_rec = db.GqlQuery("SELECT * FROM Article WHERE recommend = :recommend "
                    "ORDER BY id DESC",
                    recommend=True).fetch(10)
	context = {'articles_newest':articles_newest,
			   'articles_rec':articles_rec,
			   'category': 'home'
			   }
	return render_to_response('index.html', context)

def article(request, article_id):
	article = db.GqlQuery("SELECT * FROM Article WHERE id = :id", id=long(article_id)).get()
	meta = db.GqlQuery("SELECT * FROM Meta WHERE id = :id", id=long(article_id)).get()
	if not article:
		return HttpResponseRedirect('/')
	
	article.read_count = article.read_count + 1
	article.put()
	
	article_pre = db.GqlQuery("SELECT * FROM Article WHERE id = :id", id=long(article_id)-1).get()
	article_nxt = db.GqlQuery("SELECT * FROM Article WHERE id = :id", id=long(article_id)+1).get()
	articles_rec = db.GqlQuery("SELECT * FROM Article WHERE category = :category "
                "ORDER BY id DESC",
                category=article.category).fetch(10)
	context = {'article':article,
			   'article_pre':article_pre,
			   'article_nxt':article_nxt,
			   'articles_rec':articles_rec,
               'category':article.category,
			   'meta': meta,
               'is_admin':users.is_current_user_admin(),
			   }
        
	return render_to_response('article.html', context)

def admin(request):
	login_user = users.get_current_user()
	login_url = users.create_login_url(request.get_full_path())
	is_user_admin = users.is_current_user_admin()
	logout_url = users.create_logout_url(request.get_full_path())

	context = {'login_url':login_url,
			   'logout_url':logout_url,
			   'login_user':login_user,
			   'is_user_admin':is_user_admin
			   }
	return render_to_response('admin.html', context)

def write(request, article_id=None):
    if not users.is_current_user_admin():
        return HttpResponseRedirect('/admin/')
    article = None
    meta = None
    if article_id :
        article = db.GqlQuery("SELECT * FROM Article WHERE id = :id", id=long(article_id)).get()
        meta = db.GqlQuery("SELECT * FROM Meta WHERE id = :id", id=long(article_id)).get()
    context = {'categories':static.categories,
               'article':article,
               'meta': meta,
               }
    return render_to_response('write.html', context)


def save(request, article_id=None):
	if not users.is_current_user_admin():
		return HttpResponseRedirect('/admin/')
	if request.method == 'POST':
		if article_id:
			article = db.GqlQuery("SELECT * FROM Article WHERE id = :id", id=long(article_id)).get()
			meta = db.GqlQuery("SELECT * FROM Meta WHERE id = :id", id=long(article_id)).get()
			if not meta:
				meta = Meta()
		else:
			article = Article()
			meta = Meta()
		meta.keys = request.POST['meta_keys']	
		meta.description = request.POST['meta_description']	
		article.category = request.POST['article_category']	
		article.title = request.POST['article_title']
		article.content = db.Text(request.POST['article_content'])
		if('article_from_url' in request.POST):
			article.from_url = request.POST['article_from_url']
		if('article_reconmend' in request.POST):
				article.recommend = True  
		
		#New or update
		if article_id:
			article.put()
			meta.id = long(article_id)
			meta.put()
		else:
			meta.id = article_save(article)
			meta.put()
		return HttpResponse('''发表成功！<br/>\
							<a href="/article/write/">继续发表文章</a>\
							<a href="/">首页</a>''')

def category(requset, category, p_id=None):
	if not cmp(category.upper(), 'all'.upper()) or not cmp(category.upper(), 'newest'.upper()):
		articles_all = Article.all().order('-id')
	elif not cmp(category.upper(), 'reconmend'.upper()):
		articles_all = db.GqlQuery("SELECT * FROM Article WHERE recommend = :recommend "
				    "ORDER BY id DESC",
                    recommend=True).fetch(1000)
	else:                
		articles_all = db.GqlQuery("SELECT * FROM Article WHERE category = :category "
	                "ORDER BY id DESC",
	                category=category).fetch(1000)
	
	paginator = Paginator(articles_all, 10)
	
	try:
		page_index = int(p_id)
	except (ValueError, TypeError):
		page_index = 1
	
	try:
		articles = paginator.page(page_index)
		page_range = paginator.page_range
            	
	except (EmptyPage, InvalidPage):
		articles = paginator.page(paginator.num_pages)
        page_range = paginator.page_range
            
        if((12 in paginator.page_range) and (page_index <= 6)):
            page_range = page_range[:12]
            
        if(page_index > 6):
            page_range = page_range[(page_index-6): (page_index+6)]

	context = {'articles': articles,
               'page_range': page_range,
			   'category_title': static.category_title[category],
			   'category': category,
			   }
	return render_to_response('category.html', context)

def robots(request):
	return render_to_response('robots.txt')

