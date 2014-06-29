from .models import Seo

def seo_config(request):
	try:
		seo = Seo.objects.get(pk=1)
	except:
		seo = None
	return {
		'seo_config': seo
	}
