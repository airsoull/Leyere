from django.contrib.auth.forms import AuthenticationForm
# from registration.forms import RegistrationForm


def login_forms(request):
    if not request.user.is_authenticated():
        return {
            'login_form': AuthenticationForm,
            # 'registration_form': RegistrationForm,
        }
    return {}
