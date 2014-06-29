from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views


urlpatterns = patterns('accounts.views',
	url(r'profile/$', 'profile_detail_view', name='profile_detail_view'),
	url(r'profile/edit/$', 'profile_edit_view', name='profile_edit_view'),
    url(r'tales/$', 'story_by_user', name='story_by_user'),
    url(r'detail/(?P<slug>\w+)/$', 'author_view_detail', name='author_view_detail'),
    url(r'favorite/$', 'story_favorite_by_user', name='story_favorite_by_user'),
    url(r'register/$', 'registration_view', name='registration_register')
)

urlpatterns += patterns('',
    url(r'^password/change/$', auth_views.password_change, name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
)