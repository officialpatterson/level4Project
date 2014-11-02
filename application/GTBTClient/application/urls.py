from django.conf.urls import patterns, url
from application import views

urlpatterns = patterns('',
                       url(r'^$', views.overview, name='overview'),
                       url(r'entity/', views.entity, name='entity'),
                       url(r'search/', views.search, name='search'),
                       url(r'system/', views.system, name='system'),
                       )