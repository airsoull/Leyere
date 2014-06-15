from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'kind', 'sent')
    readonly_fields = ('email', 'kind','body', 'sent',)
    fields = ('email', 'kind', 'body', 'sent')

    def has_add_permission(self, request):
        return False

admin.site.register(Contact, ContactAdmin)
