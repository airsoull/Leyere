# -*- coding: utf-8 -*-
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

from .haystackify import haystackify

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ID = os.getenv('SITE_ID', int(1))

ADMINS = (
    (os.getenv('ADMIN_NAME', 'example'), os.getenv('ADMIN_EMAIL', 'example@example.com')),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y^fl$vj-u(4w-=*!i2kdl%^5un=_vntisz-%c7)woovwn=2!^r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

TEMPLATE_DEBUG = os.getenv('TEMPLATE_DEBUG', str(DEBUG)) == 'True'

ALLOWED_HOSTS = (os.getenv('ALLOWED_HOST', '*'),)


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',

    'accounts',
    'leyere',
    'stories',
    'contacts',
    'config',
    'api',

    'rest_framework',
    'rest_framework.authtoken',
    'registration',
    'mailqueue',
    'django_extensions',
    'south',
    'rosetta',
    'social.apps.django_app.default',
    'sorl.thumbnail',
    'bootstrapform',
    'haystack',
    'actstream',
    'mptt',
    'threadedcomments',
    'django.contrib.comments',
    'sekizai',
    # 'pipeline',

    'django.contrib.admin',  
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',
)

ROOT_URLCONF = 'leyere.urls'

WSGI_APPLICATION = 'leyere.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "leyere.context_processors.current_site",
    'accounts.context_processors.login_forms',
    'config.context_processors.seo_config',
    "stories.context_processors.category_list",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'sekizai.context_processors.sekizai',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.User', 'stories.Story', 'accounts.Profile'),
    # 'MANAGER': 'myapp.streams.MyActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    # 'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

if DEBUG:
    SHELL_PLUS = "bpython"
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += (
        'debug_toolbar',
    )


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))
}

MANAGERS = (
    (os.getenv('CONTACT_NAME', 'Contact'), os.getenv('CONTACT_EMAIL', 'contact@example.com')),
)

EMAIL_DEFAULT = os.getenv('EMAIL_DEFAULT', 'no-reply@example.com')
DEFAULT_FROM_EMAIL = EMAIL_DEFAULT

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'es')
TIME_ZONE = os.getenv('TIME_ZONE', 'America/Santiago')
USE_I18N = True
USE_L10N = True
USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ('es', gettext(u'Español')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

AUTH_USER_MODEL = 'auth.User'

ACCOUNT_ACTIVATION_DAYS = 7

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = os.getenv('STATIC_URL', '/static/')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 25))
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == 'True'

LOGIN_ERROR_URL = '/'

HAYSTACK_CONNECTIONS = {'default': haystackify(default=os.getenv('HAYSTACK_DEFAULT_CONNECTION', 'whoosh'))}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_TWITTER_KEY = os.getenv('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.getenv('SOCIAL_AUTH_TWITTER_SECRET')

PROFILE_IMAGE_AVATAR_SIZE = '100x100'
PROFILE_LARGE_IMAGE_AVATAR_SIZE = '360x360'

COMMENTS_APP = 'threadedcomments'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# HTML_MINIFY = True
# EXCLUDE_FROM_MINIFYING = ('^admin/',)