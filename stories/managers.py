from django.db import models

class StoryManager(models.Manager):
	use_for_related_fields = True

	def visible(self):
		return self.get_query_set().filter(draft=False, active=True)
	visible.queryset_method = True

	def order_visible(self):
		return self.visible().order_by('created')
	order_visible.queryset_method = True

class CategoryManager(models.Manager):
	use_for_related_fields = True

	def visible(self):
		return self.get_query_set().filter(active=True)
	# visible.queryset_method = True

	def visible_parent(self):
		return self.get_query_set().filter(active=True).filter(parent=None)
	# visible.queryset_method = True
