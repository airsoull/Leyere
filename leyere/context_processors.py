from django.contrib.sites.models import get_current_site

# from .conf import settings


def current_site(request):
    return {
        'current_site': get_current_site(request)
    }

# def default_site(request):
#     return {'default_site':settings.DEFAULT_DOMAIN}
