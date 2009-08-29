# coding: UTF-8

from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'^$',                             'views.index'),
    (r'^admin/$',                       'views.admin'),
    (r'^robots.txt$',                   'views.robots'),
    
    #发表、编辑文章
    (r'^article/write/$', 'views.write'),
    (r'^article/save/$', 'views.save'),
    #显示文章
    (r'^article/(?P<article_id>[\w-]+)/$',    'views.article'),
    (r'^category/(?P<category>[\w]+)/(?P<p_id>[\d]+)?/?$', 'views.category'),
    
    #网站图标
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/style/images/favicon.ico'}),

    #推荐文章
    (r'^reconmend/$',                       'reconmend.views.reconmend'),
    (r'^reconmend/save/$',                  'reconmend.views.save'),
    (r'^reconmend/list/$',                  'reconmend.views.list'),
    (r'^reconmend/delete/(?P<id>[\d]+)/$',  'reconmend.views.delete'),
)

