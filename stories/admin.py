from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTChangeList

from .actions import export_as_csv
from .models import Story, Category


class CategoryFilter(admin.SimpleListFilter):
    parameter_name = 'parent_category'
    title = _('Category')

    def lookups(self, request, model_admin):
        categories = Category.objects.filter(parent=None).values('pk', 'name')
        return tuple(map(lambda x: tuple(x.values()), categories))

    def queryset(self, request, queryset):
        pk = self.value()
        if pk:
            category = Category.objects.get(pk=self.value())
            queryset = queryset.filter(category__in=category.get_descendants(include_self=True))
        return queryset


class StoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('name', 'user', 'category_tree', 'anonymous', 'draft', 'active')
    list_filter = (CategoryFilter, 'anonymous', 'draft', 'active',)
    search_fields = ('name', 'user__username',)
    readonly_fields = ['user',]
    date_hierarchy = 'created'
    actions = [export_as_csv]

    def category_tree(self, instance):
        return " > ".join(map(unicode, instance.category.get_ancestors(include_self=True)))
    category_tree.short_description = _('Category')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.visible()
        return super(StoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            if 'user' not in self.readonly_fields:
                self.readonly_fields.append('user')
        else:
            if 'user' in self.readonly_fields:
                self.readonly_fields.remove('user')
        return super(StoryAdmin, self).get_form(request, obj, **kwargs)


class CategoryAdmin(admin.ModelAdmin):
    list_filter = (CategoryFilter,)
    list_display = ('name', 'order',)
    exclude = ('slug',)

    def get_changelist(self, request, **kwargs):
        return MPTTChangeList

admin.site.register(Story, StoryAdmin)
admin.site.register(Category, CategoryAdmin)
