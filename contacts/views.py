# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import Contact
from .forms import ContactForm


class ContactFormView(CreateView):
    model = Contact
    form_class = ContactForm

    def get_template_names(self):
        template_names = super(ContactFormView, self).get_template_names()
        if self.request.is_ajax():
            template_names.insert(0, 'contacts/ajax/contact_form.html')
        return template_names

    def get_initial(self):
        initial = super(ContactFormView, self).get_initial()
        kind = self.request.GET.get('kind')
        if kind:
            initial.update({'kind': kind})
        if not self.request.user.is_anonymous():
            initial.update({'email': self.request.user.email})
        return initial

    def get_success_url(self, instance=None):
        messages.success(self.request, _(u'Su Consulta Se Ha Enviado Con Éxito'))
        return reverse('contacts.views.contact_form_view')

contact_form_view = ContactFormView.as_view()
