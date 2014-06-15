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


class FilterForm(forms.Form):

    CHOICES = (('1', _(u'Creado'),), ('2', _(u'Actualizado'),))
    filter = forms.ChoiceField(label=(u'Filtro'), widget=forms.Select, choices=CHOICES, initial=2, required=True)