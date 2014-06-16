from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from stories.models import Story, Category

stories_info = {
    'queryset': Story.objects.visible(),
    'date_field': 'updated',
}

categories_info = {
	'queryset': Category.objects.visible()
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'stories': GenericSitemap(stories_info, priority=0.5, changefreq='daily',),
    'categories': GenericSitemap(categories_info, priority=0.7, changefreq='daily',),
}