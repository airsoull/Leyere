from django.conf.urls import patterns, url

urlpatterns = patterns('stories.views',
	url(r'random/$', 'story_random', name='story_random'),
	url(r'create/$', 'story_create_view', name='story_create_view'),
	url(r'update/(?P<pk>\d+)/$', 'story_update_view', name='story_update_view'),
    url(r'^(?P<category>[\w-]+)/(?P<slug>[\w-]+)-(?P<pk>\d+)/$', 'story_detail_view', name='story_detail_view'),
    url(r'^(?P<slug>[\w-]+)/$', 'story_list_by_category', name='story_list_by_category'),
    url(r'^', 'story_list', name='story_list'),
)