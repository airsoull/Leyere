# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):

    KIND_QUESTION, KIND_CATEGORY = range(2)
    KIND_CHOICES = (
        (KIND_QUESTION, _(u'Consultas')),
        (KIND_CATEGORY, _(u'Agregar Categoría')),
    )

    email = models.EmailField(_('Email'), max_length=50)
    kind = models.PositiveIntegerField(_('Contact kind'), choices=KIND_CHOICES, default=KIND_QUESTION)
    body = models.TextField(_('Body'))
    sent = models.DateTimeField(_('Sent'), auto_now_add=True)

    def __unicode__(self):
        return u'%s, %s' % (self.email, self.get_kind_display())

    def clean(self):
        self.email = self.email.strip()
        self.body = self.body.strip()