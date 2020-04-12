from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from datetime import datetime

from projects.forms import CreateEpicForm
from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic
from projects.stories.models import UserStory
from projects.tasks.models import Task
from projects.epics.services import get_epic_details, get_epics_for_user, delete_epic, get_epic_object
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

'''
-----------------------------------------------------------------------------------
Form tests
 - create
 - edit
-----------------------------------------------------------------------------------
'''

class EpicCreateFormTest(BaseTest):

    def test_create_epic_form_is_valid(self):
        '''
        The Epic creating view function's test with valid form data
        '''
        

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0],
            'description': 'Description',
            }
        form = CreateEpicForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_epic_form_invalid(self):
        '''
        The Epic creating view function's test with invalid form data
        '''
        form = CreateEpicForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

class EpicEditFormTest(BaseTest):

    def test_edit_form_valid_redirect(self):
        '''
        Checks if the editing form redirects to the desired url
        '''
        owner_prof = Profile.objects.get(user_id=self.user.id)
        epic = Epic.objects.create(name="name",project_code=Project.objects.all()[0],owner=owner_prof)

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0].pk,
            'description': 'Description',
        }
        response = self.client.post(reverse('projects:epics:epic_edit',  kwargs={'epic_id':epic.id}), form_data, follow=True)
        
        self.assertRedirects(response,reverse('projects:epics:detail', kwargs={'epic_id':epic.id}), status_code=302, target_status_code=200)


    def test_edit_form_invalid_redirect(self):
        '''
        Checks if the editing form is invalid
        '''
        owner_prof = Profile.objects.get(user_id=self.user.id)
        epic = Epic.objects.create(name="name",project_code=Project.objects.all()[0],owner=owner_prof)

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0],
            'assignee': '',
            'description': 'Description',
            'importance':'low',
            'epic': '',
        }
        response = self.client.post(reverse('projects:epics:epic_edit',  kwargs={'epic_id':epic.id}), form_data, follow=True)
        self.assertEqual(response.status_code, 200)

'''
-----------------------------------------------------------------------------------
Services tests
 - get epic details
 - get epic for a user
 - delete epic
-----------------------------------------------------------------------------------
'''

class EpicServicesTest(BaseTest):

    def test_epic_details(self):
        '''
          Checks if a basic epic created with non-optional arguments gives back the expected details.
        '''
        #test epic
        owner_prof = Profile.objects.get(user_id=self.user.id)
        epic = Epic.objects.create(name="testepic",project_code=Project.objects.all()[0],owner=owner_prof)
        

        story = UserStory.objects.create(name="testStory",project_code=Project.objects.all()[0],owner=self.user,epic=epic)
        task = Task.objects.create(name="testTask",project_code=Project.objects.all()[0],owner=self.user,epic=epic)

        test_context = get_epic_details(epic.id)

        self.assertEqual(test_context["epic"].name, epic.name)
        self.assertEqual(test_context["project"], Project.objects.all()[0])
        self.assertEqual(test_context["owner_profile"], owner_prof)
        self.assertEqual(test_context["stories"][0], story)
        self.assertEqual(test_context["tasks"][0], task)

    def test_epics_for_user(self):
        '''
          Checks for the epics which were assigned to the specified user.
        '''
        owner_prof = Profile.objects.get(user_id=self.user.id)
        epic = Epic.objects.create(name="testepic",project_code=Project.objects.all()[0],owner=owner_prof)
        epic2 = Epic.objects.create(name="testepic2",project_code=Project.objects.all()[0],owner=owner_prof)

        epics_for_user = get_epics_for_user(self.user.id)

        self.assertEqual(epics_for_user["epic_owner"][0],epic)
        self.assertEqual(epics_for_user["epic_owner"][1],epic2)
        self.assertEqual(epics_for_user["epic_owner"][0].owner, owner_prof)

    def test_delete_epic(self):
        '''
          Checks if a epic was deleted from the database.
        '''
        owner_prof = Profile.objects.get(user_id=self.user.id)
        epic = Epic.objects.create(name="testepic",project_code=Project.objects.all()[0],owner=owner_prof)

        success = delete_epic(epic.id)

        self.assertTrue(success)


'''
-----------------------------------------------------------------------------------
Views tests
 - delete epic redirect

-----------------------------------------------------------------------------------
'''

class EpicViewsTest(BaseTest):


    def test_delete_epic_redirect(self):
        """
         Test the deleting epic view.
        """
        owner_prof = Profile.objects.get(user_id=self.user.id)
        epic = Epic.objects.create(name="name",project_code=Project.objects.all()[0],owner=owner_prof)

        response = self.client.post(reverse('projects:epics:delete',  kwargs={'epic_id':epic.id}), follow=True)
        self.assertRedirects(response,reverse('users:index'))
