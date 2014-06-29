from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'email_favorite_story', 'email_comment',)
	readonly_fields = ('user',)
	list_filter = ('email_favorite_story', 'email_comment',)

	def has_add_permission(self, request):
		return False

admin.site.register(Profile, ProfileAdmin)
