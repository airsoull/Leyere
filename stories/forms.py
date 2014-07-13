from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from .models import Story, Category


class StoryForm(ModelForm):
    class Meta:
        model = Story
        fields = ('name', 'category', 'description', 'text', 'anonymous', 'draft',)

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.visible()


class StoryFormCreate(StoryForm):
    SOCIAL_CHOICES = (('1', u'Twitter',),)
    # ('2', _(u'Actualizado'),))
    social = forms.ChoiceField(label=_('Redes Sociales'), widget=forms.CheckboxSelectMultiple, choices=SOCIAL_CHOICES, required=False)

    def clean_social(self):
        # cleaned_data = super(StoryFormCreate, self).clean()
        self.socials = self.cleaned_data['social']
        print self.socials


class FilterForm(forms.Form):
    CHOICES = (('1', _(u'Creado'),), ('2', _(u'Actualizado'),))
    filter = forms.ChoiceField(label=(u'Filtro'), widget=forms.Select, choices=CHOICES, initial=2, required=True)
