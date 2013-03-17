import poohApp.models
from django.conf.urls.defaults import *
from django.views.generic import *

__author__ = 'mengmeng'
from django.conf.urls import *
import views

from models import Post
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView

urlpatterns = patterns(('poohApp.views'),


url(r'^index/$', 'index', name='index'),
url(r'^update/', 'update',name='update'),
url(r'^delete/', 'delete',name='delete'),
url(r'^register/$', views.register,name='register'),
url(r'^contact/$', views.contact,name='contact'),
url(r'^thanks/$', views.thanks,name='thanks'),
url(r'^about/$', views.about,name='about'),

# url(r'^show_homepage/$', views.show_homepage),



)




