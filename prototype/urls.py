from django.conf.urls import patterns, include, url

urlpatterns = patterns('prototype.views',
    url(r'^$', 'index'),
    url(r'^create/$', 'create'),
    url(r'^thread/(?P<thread_title>\w+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)