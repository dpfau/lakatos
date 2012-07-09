from django.conf.urls import patterns, include, url

urlpatterns = patterns('prototype.views',
    url(r'^$', 'index'),
    url(r'^create/$', 'create'),
    url(r'^thread/(?P<thread_title>\w+)/$', 'detail'),
    url(r'^author/(?P<author_name>\w+)/$', 'author'),
    url(r'^paper/(?P<paper_id>\w+)/$', 'paper')
)