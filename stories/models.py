from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.core.validators import MaxLengthValidator
from django.contrib.contenttypes import generic

from mptt.models import MPTTModel, TreeForeignKey

from .managers import StoryManager, CategoryManager


class Category(MPTTModel):
    name = models.CharField(_('Name'), max_length=50, unique=True)
    image = models.ImageField(_('Image'), blank=True, upload_to='stories/category/image', null=True)
    slug = models.SlugField(_('Slug'), max_length=255, blank=True)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, verbose_name=_('Parent'))
    description = models.TextField(_('Description'), blank=True, validators=[MaxLengthValidator(150)], help_text=_('Maximum 150 Characters'))
    active = models.BooleanField(_('Active'), default=True)
    order = models.PositiveIntegerField(_('Sort Order'), default=0)

    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.parent:
            self.slug = "%s-%s" % (self.parent.slug, self.slug)
        return super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('stories.views.story_list_by_category', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name

    def clean(self):
        self.name = self.name.strip().title()
        self.description = self.description.strip()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Story(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(_('Name'), max_length=75)
    category = TreeForeignKey('Category', verbose_name=_('Category'), related_name='story')
    description = models.TextField(_('Description'), validators=[MaxLengthValidator(150)], help_text=_('Maximum 150 Characters'))
    text = models.TextField(_('Text'))
    created = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    anonymous = models.BooleanField(_('Anonymous'), default=False)
    draft = models.BooleanField(_('Draft'), default=False)
    active = models.BooleanField(_('Active'), default=True)
    follows = generic.GenericRelation('actstream.Follow')

    objects = StoryManager()

    def __unicode__(self):
        return self.name

    def get_author(self):
        return self.user if not self.anonymous else _('Anonymous')

    def get_absolute_url(self):
        return reverse('stories.views.story_detail_view', kwargs={'category': self.category.slug, 'slug': slugify(self.name), 'pk': self.pk})

    def clean(self):
        self.name = self.name.strip()
        self.description = self.description.strip()
        self.text = self.text.strip()

    class Meta:
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')
