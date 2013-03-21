from django.conf.urls import patterns, url

urlpatterns = patterns('prototype.views',
    url(r'^$', 'index'),
    url(r'^add/(?P<thread_title>\w+)/$', 'add'),
    url(r'^link/$', 'make_link'),
    url(r'^link/(?P<node_id>\d+)/$', 'choose_link'),
    url(r'^thread/$', 'make_thread'),
    url(r'^thread/(?P<thread_title>\w+)/$', 'view_thread'),
    url(r'^author/(?P<author_name>\w+)/$', 'author'),
    url(r'^paper/(?P<paper_id>\w+)/$', 'paper'),
    url(r'^search/$', 'search'),
    url(r'^search/(?P<thread_title>\w+)/$', 'search'),
    url(r'^clear/edge/$', 'clear_edge'),
    url(r'^clear/node/$', 'clear_node'),
    url(r'^clear/thread/$', 'clear_thread'),
)