from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from projects.forms import CreateStoryForm
from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic

class StoryCreateFormTest(TestCase):

    def test_create_story_form_is_valid(self):
        '''
        The UserStoy creating view function's test with valid form data
        '''
        proj = Project(
            name='Name',
            code='CODE',
            project_owner=None,
            release='20R3'
            )

        proj.save()

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