from django.contrib import admin

from .models import Seo, PageNotFound

class SeoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    actions_on_top = False

    def has_add_permission(self, request):
        return False if Seo.objects.count() > 0 else True

admin.site.register(Seo, SeoAdmin)
admin.site.register(PageNotFound)
