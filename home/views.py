from django.views.generic import ListView
from stories.models import Story

# Create your views here.
class HomeView(ListView):
    model = Story
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        context['stories_anonymous'] = Story.objects.visible().filter(anonymous=True).order_by('created')[:10]
        return context

    def get_queryset(self):
        return Story.objects.visible().filter(anonymous=False).order_by('created')[:10]


home = HomeView.as_view()
