from django.conf.urls import patterns, url
from application import views

urlpatterns = patterns('',
                       url(r'^$', views.overview, name='overview'),
                       url(r'entity/$', views.entity, name='entity'),
                       url(r'search/$', views.search, name='search'),
                       url(r'system/$', views.system, name='system'),
                       url(r'login/$', views.user_login, name='user_login'),
		       url(r'logout/$', views.user_logout, name='user_logout'),
		       url(r'notifications/$', views.notifications, name='notifications'),
			url(r'register/$', views.register, name='register'),
                       )
