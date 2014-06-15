from .models import Seo

def seo_config(request):
	try:
		seo = Seo.objects.get()
	except:
		seo = None
	return {
		'seo_config': seo
	}
