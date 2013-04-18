from django.conf.urls import patterns, include, url
from choice import views, views_m
from django.http import HttpResponse



def welcome(request):
    return HttpResponse('Welcome to ChoiceSite!')

urlpatterns = patterns('',
    (r'^$', welcome),
)

urlpatterns += patterns('',
    url(r'^index/$', views.index, name='index'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^result/$', views.result, name='result'),
    url(r'^detail/$', views.detail, name='detail')
)

urlpatterns += patterns('',
    url(r'^m/login/$', views_m.login, name='login_m'),
    url(r'^m/register/$', views_m.register, name='register_m'),
    url(r'^m/post/$', views_m.post, name='post_m'),
    url(r'^m/vote/$', views_m.vote, name='vote_m'),
    url(r'^m/index/$', views_m.index, name='index_m'),
    url(r'^m/detail/$', views_m.detail, name='detail_m'),
    url(r'^m/profile/$', views_m.profile, name='profile_m'),
)





