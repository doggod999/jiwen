#coding=utf-8

from __future__ import division
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response

from google.appengine.api import users
from google.appengine.ext import db

from models import Reconmend

def reconmend_save(reconmend):
    id = 0
    try:
        reconmends = Reconmend.all().order('-id')
        id = reconmends[0].id + 1
    except:
        id = 1
    reconmend.id = id
    reconmend.put()

def reconmend(request):
	return render_to_response('reconmend/urlinput.html')

def save(request):
	url = request.POST['url']
	if not url or not cmp(url.upper(), 'http://'.upper()):
		context={'message':'链接地址不能为空',
				 }
		return render_to_response('reconmend/urlinput.html', context)
	elif not url.startswith('http://'):	
		context={'message':'链接地址必须要以http://开头',
				 }
		return render_to_response('reconmend/urlinput.html', context)
	else:	
		reconmend = Reconmend()
		reconmend.url = request.POST['url']
		reconmend_save(reconmend)
		return render_to_response('reconmend/success.html')

def list(request):
	if not users.is_current_user_admin():
		return HttpResponseRedirect('/admin/')
	
	reconmends = Reconmend.all().fetch(1000)
	context = {'reconmends':reconmends
			   }	
	return render_to_response('reconmend/list.html', context)

def delete(request, id):
	if not users.is_current_user_admin():
		return HttpResponseRedirect('/admin/')
	
	reconmend = db.GqlQuery("SELECT * FROM Reconmend WHERE id = :id", id=long(id)).get()
	reconmend.delete()
	return HttpResponseRedirect('/reconmend/list/')
	


