import unicodedata
import re

from django.views.generic import ListView
from django.db.models import Q

from stories.models import Story


class SearchList(ListView):
    model = Story
    value = None
    template_name = 'search/search.html'

    def name_normalize(self, queryset):
        name = ''.join((c for c in unicodedata.normalize('NFD', queryset.name) if unicodedata.category(c) != 'Mn'))
        return name.lower()

    def dict_name_normalize_pk(self):
        querysets = Story.objects.visible()
        array_pk = []
        for queryset in querysets:
            if re.search(r".%s."% self.value, self.name_normalize(queryset)):
                array_pk.append(queryset.pk)
            if re.search(r"%s."% self.value, self.name_normalize(queryset)):
                array_pk.append(queryset.pk)
            if re.search(r".%s"% self.value, self.name_normalize(queryset)):
                array_pk.append(queryset.pk)
        return array_pk

    def get_queryset(self):
        self.value = self.request.GET.get('q', None)
        value = self.value

        if value:
            queryset = Story.objects.visible().filter(
                Q(pk__in=self.dict_name_normalize_pk())|
                Q(name__icontains=value)|
                Q(category__name__icontains=value)|
                Q(description__icontains=value)|
                Q(text__icontains=value)
                ).annotate()
        else:
            queryset = []
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchList, self).get_context_data(kwargs=kwargs)
        context['value'] = self.value
        return context

search_list = SearchList.as_view()
