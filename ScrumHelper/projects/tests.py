from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from datetime import datetime

from projects.forms import CreateProjectForm
from projects.models import Project, Documents
from users.models import Profile
from projects.epics.models import Epic
from projects.tasks.models import Task
from projects.issues.models import Issue
from projects.stories.models import UserStory
from projects.services import delete_project, get_issues_for_project
from django.contrib.auth.models import User


class BaseTest(TestCase):
    def setUp(self):
        superuser = User.objects.create_superuser(
            'test', 'test@api.com', 'testpassword')
        self.user = superuser
        self.client.login(username=superuser.username, password='testpassword')


'''
-----------------------------------------------------------------------------------
Form tests
 - create
 - edit
-----------------------------------------------------------------------------------
'''

class ProjectCreateFormTest(BaseTest):

    def test_create_project_form_is_valid(self):
        '''
        The Project creating view function's test with valid form data
        '''
        form_data = {
            'name':'New',
            'code':'TEST',
            'release': '2020',
            }
        form = CreateProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_project_form_invalid(self):
        '''
        The UserStoy creating view function's test with invalid form data
        '''
        form = CreateProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

class ProjectEditFormTest(BaseTest):

    def test_edit_form_valid_redirect(self):
        '''
        Checks if the editing form redirects to the desired url
        '''

        project = Project.objects.create(name="test",code='TEST',project_owner=self.user)

        form_data = {
            'name':'New',
            'code':'TEST',
            'release': '2020',
        }
        response = self.client.post(reverse('projects:project_edit',  kwargs={'project_id':project.id}), form_data, follow=True)
        
        self.assertRedirects(response,reverse('projects:detail', kwargs={'project_id':project.id}), status_code=302, target_status_code=200)


    def test_edit_form_invalid_redirect(self):
        '''
        Checks if the editing form is invalid
        '''

        project = Project.objects.create(name="name",code='TEST',project_owner=self.user)

        form_data = {
            'name':'New',
            'code':'TEST',
            'release': '2020',
        }
        response = self.client.post(reverse('projects:project_edit',  kwargs={'project_id':project.id}), form_data, follow=True)
        self.assertEqual(response.status_code, 200)

'''
-----------------------------------------------------------------------------------
Services tests
 - get issues for a project
 - delete project
-----------------------------------------------------------------------------------
'''

class ProjectServicesTest(BaseTest):

    def test_project_details(self):
        '''
          Checks if a basic project created with non-optional arguments gives back the expected details.
        '''
        #test project
        project = Project.objects.create(name="name",code='TEST',project_owner=self.user)
        owner_prof = Profile.objects.get(user_id=self.user.id)

        epic = Epic.objects.create(name="epic", project_code=project,owner=owner_prof)
        task = Task.objects.create(name="task", project_code=project,owner=self.user)

        test_context = get_issues_for_project(project.id)

        self.assertEqual(test_context["project"].name, project.name)
        self.assertEqual(test_context["epic_list"][0], epic)
        self.assertEqual(test_context["task_list"][0], task)
        self.assertEqual(test_context["project"].project_owner, self.user)

    def test_delete_project(self):
        '''
          Checks if a project was deleted from the database.
        '''
        project = Project.objects.create(name="name",code='TEST',project_owner=self.user)

        success = delete_project(project.id)

        self.assertTrue(success)

'''
-----------------------------------------------------------------------------------
Views tests
 - add document
 - delete document
 - delete project redirect
 - kanban board
-----------------------------------------------------------------------------------
'''

class ProjectViewsTest(BaseTest):

    def test_upload_document_view_redirect(self):
        """
        Tests if the Upload document gets the input file-> uploads the document->saves it-> then redirects to the projects's detail page.
        """

        project = Project.objects.create(name="name",code='TEST',project_owner=self.user)

        f = open("test.txt","w+")

        for i in range(10):
            f.write("This is line %d\r\n" % (i+1))

        f.close() 

        with open("test.txt") as fp:
           response = self.client.post(reverse('projects:upload_doc', kwargs={'project_id':project.id}), {'name': 'test.txt', 'attachment': fp}, follow=True)
        self.assertRedirects(response,reverse('projects:detail', kwargs={'project_id':project.id}), status_code=302, target_status_code=200)

    #def test_delete_document_view(self):

    def test_delete_project_redirect(self):
        """
         Test the deleting task view.
        """
        project = Project.objects.create(name="name",code='TEST',project_owner=self.user)

        response = self.client.post(reverse('projects:delete',  kwargs={'project_id':project.id}), follow=True)
        self.assertRedirects(response,reverse('projects:index'), status_code=302, target_status_code=200)


    def test_kanban_view(self):
        """
         Tests the kanban board view.
        """
        project = Project.objects.create(name="name",code='TEST',project_owner=self.user)

        story = UserStory.objects.create(name="testStory", project_code=project, owner=self.user, state="OPEN")
        task = Task.objects.create(name="testTask", project_code=project, owner=self.user, state="IN PROGRESS")
        issue = Issue.objects.create(name="testIssue", project_code=project, owner=self.user, state="TESTING", defect_type="BUG")

        response = self.client.get(reverse('projects:kanban_board'))

        self.assertEqual(len(response.context["open_stories"]), 1)
        self.assertEqual(len(response.context["inprogress_tasks"]), 1)
        self.assertEqual(len(response.context["testing_issues"]), 1)