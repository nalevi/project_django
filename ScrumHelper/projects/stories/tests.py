from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from projects.forms import CreateStoryForm
from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic
from projects.stories.models import UserStory
from django.contrib.auth.models import User


class BaseTest(TestCase):
    def setUp(self):
        superuser = User.objects.create_superuser(
            'test', 'test@api.com', 'testpassword')
        self.user = superuser
        self.client.login(username=superuser.username, password='testpassword')
        proj = Project.objects.create(
            name='Name',
            code='CODE',
            project_owner=None,
            release='20R3'
            )


class StoryCreateFormTest(BaseTest):

    def test_create_story_form_is_valid(self):
        '''
        The UserStoy creating view function's test with valid form data
        '''
        

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0],
            'assignee': None,
            'description': 'Description',
            'importance':'low',
            'epic': None,
            }
        form = CreateStoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_story_form_invalid(self):
        '''
        The UserStoy creating view function's test with invalid form data
        '''
        form = CreateStoryForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

class StoryEditFormTest(BaseTest):

    def test_edit_form_valid_redirect(self):
        '''
        Checks if the editing form redirects to the desired url
        '''

        story = UserStory.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0].pk,
            'assignee': '',
            'description': 'Description',
            'importance':'low',
            'epic': '',
        }
        response = self.client.post(reverse('projects:stories:story_edit',  kwargs={'story_id':story.id}), form_data, follow=True)
        
        self.assertRedirects(response,reverse('projects:stories:detail', kwargs={'story_id':story.id}), status_code=302, target_status_code=200)


    def test_edit_form_invalid_redirect(self):
        '''
        Checks if the editing form is invalid
        '''

        story = UserStory.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0],
            'assignee': '',
            'description': 'Description',
            'importance':'low',
            'epic': '',
        }
        response = self.client.post(reverse('projects:stories:story_edit',  kwargs={'story_id':story.id}), form_data, follow=True)
        self.assertEqual(response.status_code, 200)