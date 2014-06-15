from haystack import indexes
from stories.models import Story


class StorySearchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField()
    description = indexes.CharField()
    text = indexes.CharField()
    category = indexes.CharField(model_attr='category')

    def get_model(self):
        return Story

    def index_queryset(self, using=None):
        return self.get_model().objects.visible()
# site.register(Story, StorySearchIndex)
