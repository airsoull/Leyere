from .models import Category

def category_list(request):
	return {
		'category_list': Category.objects.visible_parent().order_by('order')
	}
