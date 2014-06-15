from django.conf.urls import patterns, url

urlpatterns = patterns('search.views',
    url(r'^$', 'search_list', name='search_list'),
)