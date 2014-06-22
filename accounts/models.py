from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
# from django.contrib.comments.models import Comment

from django_countries.fields import CountryField
from sorl.thumbnail import get_thumbnail
from registration.signals import user_activated
from threadedcomments.models import ThreadedComment
from actstream.models import Follow

from .conf import settings
from stories.models import Story


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    user_slug = models.SlugField(_('Slug'), editable=False, null=True)
    photo = models.ImageField(_('Photo'), blank=False, upload_to='accounts/profile/avatar', null=True)
    country = CountryField(_('Country'), blank=True)
    location = models.CharField(_('Location'), max_length=140, blank=True)
    about = models.TextField(_('About'), blank=True, validators=[MaxLengthValidator(150)], help_text=_('Maximum 150 Characters'))
    follows = generic.GenericRelation('actstream.Follow')

    def liked_stories(self):
        content_type = ContentType.objects.get_for_model(Story)
        return self.user.follow_set.filter(content_type=content_type)

    def get_absolute_url(self):
        return reverse('accounts.views.author_view_detail', kwargs={'slug': self.user_slug})

    @property
    def image_avatar_url(self):
        im = get_thumbnail(self.photo, settings.PROFILE_IMAGE_AVATAR_SIZE, crop="center")
        return im.url

    @property
    def image_avatar_large_url(self):
        im = get_thumbnail(self.photo, settings.PROFILE_LARGE_IMAGE_AVATAR_SIZE, crop="center")
        return im.url

    def __unicode__(self):
        return self.user.username

@receiver(post_save, sender=Follow, dispatch_uid='send_email_by_favorite_story')
def send_email_by_favorite_story(sender, instance, created, **kwargs):
    if created:
        from django.template.loader import render_to_string
        subject = _('Han marcado como favorita una de tus historias') + ' - ' + 'Leyere.com'
        from_address = settings.EMAIL_DEFAULT
        to_address = instance.follow_object.user.email
        content = render_to_string("actstream/email/email_favorite.txt", {'favorite': instance})
        try:
            from mailqueue.models import MailerMessage
            msg = MailerMessage()
            msg.subject = subject
            msg.to_address = to_address
            msg.from_address = from_address
            msg.content = content
            msg.app = 'Favorite Story'
            msg.send_mail()
        except ImportError:
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, content, from_address, to_address)
            msg.send()

@receiver(post_save, sender=ThreadedComment, dispatch_uid='send_email_by_comment')
def send_email_by_comment(sender, instance, created, **kwargs):
    if created:
        from django.template.loader import render_to_string
        subject = _('Nuevo Comentario') + ' - ' + 'Leyere.com' 
        from_address = settings.EMAIL_DEFAULT
        to_address = instance.user_email
        content = render_to_string("comments/email/email_comment.txt", {'comment': instance})
        try:
            from mailqueue.models import MailerMessage
            msg = MailerMessage()
            msg.subject = subject
            msg.to_address = to_address
            msg.from_address = from_address
            msg.content = content
            msg.app = 'Comment'
            msg.send_mail()
        except ImportError:
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject, content, from_address, to_address)
            msg.send()

@receiver(post_save, sender=User, dispatch_uid='create_profile_on_created_user')
def create_profile_on_created_user(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.user_slug = slugify(instance.username)
        profile.save()
        from rest_framework.authtoken.models import Token
        Token.objects.create(user=instance)

def login_on_activation(sender, user, request, **kwargs):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

user_activated.connect(login_on_activation, dispatch_uid="loginonactivation")