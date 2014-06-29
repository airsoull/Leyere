from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from threadedcomments.models import ThreadedComment

from registration.forms import RegistrationFormUniqueEmail

from .forms import ProfileForm
from stories.tests import create_user, create_story, create_category


class ProfileDetailTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.url = reverse('accounts.views.profile_detail_view')

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url, target_status_code=200)
        response = self.client.post(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url, target_status_code=200)

    def test_get(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_detail.html')
        self.assertIn('user', response.context)
        self.assertEqual(self.user.profile, response.context['object'])

    # def test_valid_form(self):
    #     image = open('accounts/profile/avatar/image.png', 'rb')
    #     param_image = {'photo': SimpleUploadedFile(image.name, image.read())}
    #     params = {
    #         'user': self.user.id,
    #         'location': 'lorem ipsum',
    #         'about': 'lorem ipsum-description',
    #     }
    #     form = ProfileForm(params, param_image)
    #     self.assertEqual(form.is_valid(), True)

    # def test_post(self):
    #     self.client.login(username=self.user.username, password='password')
    #     image = open('accounts/profile/avatar/image.png', 'rb')
    #     param_image = {'photo': SimpleUploadedFile(image.name, image.read())}
    #     params = {
    #         'user': self.user.id,
    #         'photo': 'img.jpg',
    #         'location': 'lorem ipsum',
    #         'about': 'lorem ipsum-description',
    #     }
    #     response = self.client.post(self.url, params, param_image)
    #     profile = Profile.objects.get()
    #     self.assertRedirects(response, reverse('accounts.views.profile_edit_view'), target_status_code=200)
    #     self.assertEqual(params['photo'], profile.photo)
    #     self.assertEqual(params['location'], profile.location)
    #     self.assertEqual(params['about'], profile.about)


class ProfileEditView(TestCase):

    def setUp(self):
        self.user = create_user()
        self.url = reverse('accounts.views.profile_edit_view')

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url, target_status_code=200)
        response = self.client.post(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url, target_status_code=200)

    def test_get(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ProfileForm)
        self.assertTemplateUsed(response, 'accounts/profile_form.html')


class StoryByUserTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.url = reverse('accounts.views.story_by_user')

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url, target_status_code=200)
        response = self.client.post(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url, target_status_code=200)

    def test_get(self):
        category = create_category()
        user2 = create_user(username='user')

        story = create_story(user=self.user, category=category)
        story2 = create_story(user=user2, category=category)

        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/tale_user_list.html')
        self.assertIn('user', response.context)
        self.assertIn(story, response.context['object_list'])
        self.assertNotIn(story2, response.context['object_list'])


class AuthorDetailView(TestCase):

    def setUp(self):
        self.user = create_user()
        self.url = reverse('accounts.views.author_view_detail', kwargs={'slug': slugify(self.user.username)})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_detail_public.html')
        self.assertIn('user', response.context)
        self.assertEqual(self.user.profile, response.context['object'])


class StoryFavoriteView(TestCase):

    def setUp(self):
        self.user = create_user()
        self.url = reverse('accounts.views.story_favorite_by_user')

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url, target_status_code=200)
        response = self.client.post(self.url)
        self.assertRedirects(response, 'accounts/login/?next=%s'%self.url, target_status_code=200)

    def test_get(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.context)
        self.assertEqual(self.user.profile, response.context['object'])
        self.assertTemplateUsed(response, 'accounts/profile_favorite_story.html')


class RegistrationView(TestCase):

    def setUp(self):
        self.url = reverse('accounts.views.registration_view')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegistrationFormUniqueEmail)
        self.assertTemplateUsed(response, 'registration/registration_form.html')


class CommentSendEmail(TestCase):
    
    def test_create_comment(self):
        comment = ThreadedComment.objects.create()
        print comment
