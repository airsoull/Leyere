from django.conf import settings as django_settings


class Settings(object):
    @property
    def PROFILE_IMAGE_AVATAR_SIZE(self):
        return getattr(django_settings, 'PROFILE_IMAGE_AVATAR_SIZE', '100x100')

    @property
    def PROFILE_LARGE_IMAGE_AVATAR_SIZE(self):
        return getattr(django_settings, 'PROFILE_LARGE_IMAGE_AVATAR_SIZE', '200x200')

    @property
    def AUTH_USER_MODEL(self):
        return getattr(django_settings, 'AUTH_USER_MODEL', django_settings.AUTH_USER_MODEL)

    @property
    def EMAIL_DEFAULT(self):
    	return getattr(django_settings, 'EMAIL_DEFAULT', django_settings.EMAIL_DEFAULT)

settings = Settings()
