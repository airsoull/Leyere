# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import Story, Category
from .forms import StoryForm, StoryFormCreate


class StoryDetail(DetailView):
    model = Story

    def get_object(self):
        return super(StoryDetail, self).get_object()

    def get_queryset(self):
        return Story.objects.visible()

story_detail_view = StoryDetail.as_view()


class StoryList(ListView):
    model = Story

    def get_queryset(self):
        return Story.objects.order_visible()

story_list = StoryList.as_view()


class StoryListByCategory(StoryList):
    paginate_by = 10
    #template_name = 'story/story_list_by_category.html'

    def dispatch(self, request, slug):
        self.category = get_object_or_404(Category, slug=slug)
        return super(StoryListByCategory, self).dispatch(request=request, slug=slug)

    def get_context_data(self, **kwags):
        context = super(StoryListByCategory, self).get_context_data()
        context['category'] = self.category
        return context

    def get_queryset(self):
        return super(StoryListByCategory, self).get_queryset().filter(category=self.category)

story_list_by_category = StoryListByCategory.as_view()


class StoryRandom(RedirectView):
    permanent = False

    def get_redirect_url(self):
        try:
            story = Story.objects.visible().order_by('?')[0]
        except IndexError:
            raise Http404
        return story.get_absolute_url()

story_random = StoryRandom.as_view()


class StoryCreateView(CreateView):
    model = Story
    form_class = StoryFormCreate
    template_name = 'stories/create_story_form.html'

    @method_decorator(login_required)
    def dispatch(self, request):
        return super(StoryCreateView, self).dispatch(request=request)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        print '*'*10
        print form.social
        print '*'*10
        return super(StoryCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _(u'Se Ha Creado Con Éxito'))
        return super(StoryCreateView, self).get_success_url() if not self.object.draft else reverse('story_update_view', kwargs={'pk': self.object.pk})

story_create_view = StoryCreateView.as_view()


class StoryUpdateView(UpdateView):
    model = Story
    form_class = StoryForm
    template_name = 'stories/update_story_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, pk):
        return super(StoryUpdateView, self).dispatch(request=request)

    def get_queryset(self):
        return super(StoryUpdateView, self).get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        messages.success(self.request, _(u'Se Ha Actualizado Con Éxito'))
        return super(StoryUpdateView, self).get_success_url() if not self.object.draft else reverse('stories.views.story_update_view', kwargs={'pk': self.object.pk})

story_update_view = StoryUpdateView.as_view()
