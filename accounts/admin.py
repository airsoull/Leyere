from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user',)
	readonly_fields = ('user',)

	def has_add_permission(self, request):
		return False

admin.site.register(Profile, ProfileAdmin)
