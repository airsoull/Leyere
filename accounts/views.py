# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import Profile
from .forms import ProfileForm

from stories.models import Story


class ProfileDetail(DetailView):
    model = Profile

    @method_decorator(login_required)
    def dispatch(self, request):
        return super(ProfileDetail, self).dispatch(request=request)

    def get_object(self, queryset=None):
        profile, self.created = Profile.objects.get_or_create(user=self.request.user)
        return profile

profile_detail_view = ProfileDetail.as_view()


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileForm

    @method_decorator(login_required)
    def dispatch(self, request):
        return super(ProfileEditView, self).dispatch(request=request)

    def get_object(self, queryset=None):
        profile, self.created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self, instance=None):
        messages.success(self.request, _(u'Sus Datos Se Han Actualizado Con Éxito'))
        return reverse('accounts.views.profile_edit_view')

profile_edit_view = ProfileEditView.as_view()


class StoryByUser(ListView):
    model = Story
    template_name = 'accounts/tale_user_list.html'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request):
        return super(StoryByUser, self).dispatch(request=request)

    def get_queryset(self):
        return super(StoryByUser, self).get_queryset().filter(user=self.request.user)

story_by_user = StoryByUser.as_view()


class AuthorViewDetail(DetailView):
    model = Profile
    slug_field = 'user_slug'
    template_name = 'accounts/profile_detail_public.html'

author_view_detail = AuthorViewDetail.as_view()


class StoryFavoriteByUser(DetailView):
    model = Profile
    template_name = 'accounts/profile_favorite_story.html'

    @method_decorator(login_required)
    def dispatch(self, request):
        return super(StoryFavoriteByUser, self).dispatch(request=request)

    def get_object(self, queryset=None):
        profile, self.created = Profile.objects.get_or_create(user=self.request.user)
        return profile

story_favorite_by_user = StoryFavoriteByUser.as_view()