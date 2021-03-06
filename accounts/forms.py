from django.forms import ModelForm

from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'about', 'email_comment')