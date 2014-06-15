from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from .models import Story, Category
from .forms import StoryForm


def create_user(email='admin@example.net', password='password', username="admin"):
    return User.objects.create_user(email=email, password=password, username=username)  

def create_category(name='category-test'):
    return Category.objects.create(name=name)

def create_story(user, name='bar', description='foo-bar', text='foo-bar-text', category=None, **kwargs):
    return Story.objects.create(user=user, name=name, description=description, text=text, category=category, **kwargs)


class StoryModelTest(TestCase):
    
    def setUp(self):
        self.user = create_user()
        self.category = create_category()
        self.story = create_story(user=self.user, category=self.category)
        self.url = reverse('stories.views.story_detail_view', kwargs={'category': slugify(self.category.name), 'slug': slugify(self.story.name), 'pk': self.story.pk})

    def test_absolute_url(self):
        self.assertEqual(self.url, self.story.get_absolute_url())

    def test_no_anonymous(self):
        self.assertEqual(str(self.story.get_author()), self.story.user.username)

    def test_anonymous(self):
        self.story.anonymous = True
        self.story.save()
        self.assertEqual(self.story.get_author(), _('Anonymous'))


class CategoryModelTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.category = create_category()
        self.url = reverse('stories.views.story_list_by_category', kwargs={'slug': self.category.slug})

    def test_absolute_url(self):
        self.assertEqual(self.url, self.category.get_absolute_url())

    def test_save_model(self):
        self.category.name = 'NEW NAME'
        self.category.save()
        self.assertEqual(self.category.slug, 'new-name')


class DetailStoryTest(TestCase):
    
    def setUp(self):
        self.user = create_user()
        self.category = create_category()
        story = create_story(user=self.user, category=self.category)
        self.url = reverse('stories.views.story_detail_view', kwargs={'category': slugify(self.category.name), 'slug': slugify(story.name), 'pk': story.pk})

    def test_get(self):
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'stories/story_detail.html')

    def test_anonymous(self):
        story = create_story(user=self.user, category=self.category, anonymous=True)
        self.url = reverse('stories.views.story_detail_view', kwargs={'category': slugify(self.category.name), 'slug': slugify(story.name), 'pk': story.pk})
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

    def test_draft(self):
        story = create_story(user=self.user, category=self.category, draft=True)
        self.url = reverse('stories.views.story_detail_view', kwargs={'category': slugify(self.category.name), 'slug': slugify(story.name), 'pk': story.pk})
        response = self.client.get(self.url)

        self.assertEqual(404, response.status_code)


class ListCategory(TestCase):

    def setUp(self):
        self.category = create_category()
        self.user = create_user()
        self.url = reverse('stories.views.story_list_by_category', kwargs={'slug': self.category.slug})

    def test_get(self):
        category2 = create_category(name='bar')
        story1 = create_story(user=self.user, category=self.category)
        story2 = create_story(user=self.user, name='tale-test' ,category=category2)
        story3 = create_story(user=self.user, category=self.category, draft=True)
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'stories/story_list.html')
        self.assertIn(story1, response.context['story_list'])
        self.assertNotIn(story2, response.context['story_list'])
        self.assertNotIn(story3, response.context['story_list'])

    def test_no_category(self):
        url = reverse('stories.views.story_list_by_category', kwargs={'slug': 'none'})
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)


class RedirectStory(TestCase):
    
    def setUp(self):
        self.url = reverse('stories.views.story_random')

    def test_get(self):
        self.user = create_user()
        self.category = create_category()
        self.story = create_story(user=self.user, category=self.category)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.story.get_absolute_url(), status_code=302)

    def test_no_story(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class CreateStory(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='admin@example.net', password='password', username="admin")
        self.user = User.objects.get(pk=self.user.pk)
        self.category = create_category()
        self.url = reverse('stories.views.story_create_view')

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url)

    def test_get(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_form(self):
        params = {
            'user': self.user.id,
            'name': 'test-story',
            'category': self.category.id,
            'description': 'description',
            'text': 'text lorem ipsum',
        }
        form = StoryForm(params)
        self.assertEqual(form.is_valid(), True)

    def test_invalid_form(self):
        params = {
            'user': self.user.id,
            'name': '',
            'category': '',
            'description': '',
            'text': '',
        }
        form = StoryForm(params)
        self.assertEqual(form.is_valid(), False)

    def test_post(self):
        self.client.login(username=self.user.username, password='password')

        params = {
            'user': self.user.id,
            'name': 'test-story',
            'category': self.category.id,
            'description': 'description',
            'text': 'text lorem ipsum',
            'draft': False,
        }
        self.assertEqual(Story.objects.count(), 0)
        response = self.client.post(self.url, params, follow=True)
        self.assertEqual(Story.objects.count(), 1)
        story = Story.objects.get()
        self.assertRedirects(response, reverse('stories.views.story_detail_view', kwargs={'category': slugify(self.category.name), 'slug': slugify(story.name), 'pk': story.pk}), target_status_code=200)

    def test_post_draft(self):
        self.client.login(username=self.user.username, password='password')

        params = {
            'user': self.user.id,
            'name': 'test-story',
            'category': self.category.id,
            'description': 'description',
            'text': 'text lorem ipsum',
            'draft': True
        }
        self.assertEqual(Story.objects.count(), 0)
        response = self.client.post(self.url, params, follow=True)
        self.assertEqual(Story.objects.count(), 1)
        story = Story.objects.get()
        self.assertRedirects(response, reverse('stories.views.story_update_view', kwargs={'pk': story.pk}), target_status_code=200)

class UpdateStory(TestCase): 
    
    def setUp(self):
        self.user = User.objects.create_user(email='admin@example.net', password='password', username="admin")
        self.user = User.objects.get(pk=self.user.pk)
        self.category = create_category()
        self.story = create_story(user=self.user, category=self.category)
        self.url = reverse('stories.views.story_update_view', kwargs={'pk': self.story.pk})

    def test_get(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse('stories.views.story_update_view', kwargs={'pk': self.story.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stories/update_story_form.html')

    def test_get_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url)

    def test_post(self):
        self.client.login(username=self.user.username, password='password')
        params = {
            'user': self.user.id,
            'name': 'new name',
            'category': self.category.id,
            'description': 'new description',
            'text': 'new text',
            'draft': False,
        }
        response = self.client.post(self.url, params)
        story = Story.objects.get()
        self.assertRedirects(response, reverse('stories.views.story_detail_view', kwargs={'category': slugify(self.category.name), 'slug': slugify(story.name), 'pk': story.pk}), target_status_code=200)
        self.assertEqual(params['name'], story.name)
        self.assertEqual(params['description'], story.description)
        self.assertEqual(params['text'], story.text)
        self.assertEqual(params['draft'], story.draft)

    def test_post_is_draft(self):
        self.client.login(username=self.user.username, password='password')
        params = {
            'user': self.user.id,
            'name': 'new name',
            'category': self.category.id,
            'description': 'new description',
            'text': 'new text',
            'draft': True,
        }
        response = self.client.post(self.url, params)
        story = Story.objects.get()
        self.assertRedirects(response, self.url, target_status_code=200)
        self.assertEqual(params['name'], story.name)
        self.assertEqual(params['description'], story.description)
        self.assertEqual(params['text'], story.text)
        self.assertEqual(params['draft'], story.draft)
