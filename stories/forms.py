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
    social = forms.MultipleChoiceField(label=_('Redes Sociales'), widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, user, *args, **kwargs):
        SOCIAL_CHOICES = [(social.provider, social.provider) for social in user.social_auth.all()]
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.visible()
        self.fields['social'].choices = SOCIAL_CHOICES # user.social_auth.values('provider').all()

class FilterForm(forms.Form):
    CHOICES = (
        (0, 'a'),
        (1, 'b'),
        (2, 'c'),
    )
    filter = forms.MultipleChoiceField(label=(u'Filtro'), widget=forms.CheckboxSelectMultiple, choices=CHOICES, required=False)
