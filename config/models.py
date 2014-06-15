from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxLengthValidator


class Seo(models.Model):
	title = models.CharField(_('Title'), max_length=50)
	description = models.TextField(_('Description'), validators=[MaxLengthValidator(150)])

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = _('SEO')
        verbose_name_plural = _('SEO')

class PageNotFound(models.Model):
	author = models.CharField(_('Author'), max_length=50, blank=False)
	url = models.URLField(_('Url'), blank=False, max_length=100)
	image = models.ImageField(_('Image'), upload_to='config/page', blank=False)
	active = models.BooleanField(_('Active'), default=True)

	def __unicode__(self):
		return self.author

	class Meta:
		verbose_name = _('Page Not Found')
		verbose_name_plural = _('Page Not Found')
