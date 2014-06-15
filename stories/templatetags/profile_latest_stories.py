from django import template
from stories.models import Story

register = template.Library()


@register.inclusion_tag('accounts/_latest_stories.html')
def profile_latest_stories(profile):
    stories = Story.objects.visible().filter(user=profile, anonymous=False).order_by('created')[:10]
    return {'stories': stories}
