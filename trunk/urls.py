# coding: UTF-8

from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'^$',                             'views.index'),
    (r'^login/$',                       'views.login'),
    (r'^robots.txt$',                   'views.robots'),
    
    #发表、编辑文章
    (r'^article/write/$', 'views.write'),
    (r'^article/save/$', 'views.save'),
    #显示文章
    (r'^article/(?P<article_id>[\w-]+)/$',    'views.article'),
    (r'^category/(?P<category>[\w]+)/(?P<p_id>[\d]+)?/?$', 'views.category'),
    
    #网站图标
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/style/images/favicon.ico'}),

)

