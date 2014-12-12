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
                       url(r'addtrack/$', views.addtrack, name='add_track'),
                       url(r'untrack/$', views.untrack, name='un_track'),
                       url(r'viewtracks/$', views.viewtracks, name='view_tracks'),
                       url(r'compare/$', views.compare, name='compare'),
                       url(r'notifications/$', views.notifications, name='notifications'),
                       url(r'addnotification/$', views.addnotification, name='addnotification'),
                       url(r'vwn/$', views.viewnotifications, name='viewnotifications'),
                       )
