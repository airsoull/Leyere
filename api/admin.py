from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin


class TokenAdmin(TokenAdmin):
	readonly_fields = ('user',)

	def has_add_permission(self, request):
		return False


class TokenInline(admin.StackedInline):
    model = Token
    readonly_fields = ['key',]


class ApiUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [TokenInline]


admin.site.unregister(User)
admin.site.unregister(Token)
admin.site.register(User, ApiUserAdmin)
admin.site.register(Token, TokenAdmin)