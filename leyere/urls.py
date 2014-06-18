import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin

from sitemaps import sitemaps
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('home.urls')),
    url(r'^story/', include('stories.urls')),
    url(r'^contact/', include('contacts.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^rosetta/', include('rosetta.urls')),
    # url(r'^search/', include('haystack.urls')),
    url(r'^activity/', include('actstream.urls')),
    url(r'^articles/comments/', include('django.contrib.comments.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^Sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT})
    )