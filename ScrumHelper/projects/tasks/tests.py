from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from datetime import datetime

from projects.forms import CreateTaskForm
from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic
from projects.tasks.models import Task
from projects.tasks.services import get_task_details, get_tasks_for_user, delete_task, change_task_state, get_task_object
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

class TaskCreateFormTest(BaseTest):

    def test_create_task_form_is_valid(self):
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
        form = CreateTaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_task_form_invalid(self):
        '''
        The UserStoy creating view function's test with invalid form data
        '''
        form = CreateTaskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

class TaskEditFormTest(BaseTest):

    def test_edit_form_valid_redirect(self):
        '''
        Checks if the editing form redirects to the desired url
        '''

        task = Task.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0].pk,
            'assignee': '',
            'description': 'Description',
            'importance':'low',
            'epic': '',
        }
        response = self.client.post(reverse('projects:tasks:task_edit',  kwargs={'task_id':task.id}), form_data, follow=True)
        
        self.assertRedirects(response,reverse('projects:tasks:detail', kwargs={'task_id':task.id}), status_code=302, target_status_code=200)


    def test_edit_form_invalid_redirect(self):
        '''
        Checks if the editing form is invalid
        '''

        task = Task.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0],
            'assignee': '',
            'description': 'Description',
            'importance':'low',
            'epic': '',
        }
        response = self.client.post(reverse('projects:tasks:task_edit',  kwargs={'task_id':task.id}), form_data, follow=True)
        self.assertEqual(response.status_code, 200)

'''
-----------------------------------------------------------------------------------
Services tests
 - get task details
 - get storis for a user
 - delete task
 - change task state
-----------------------------------------------------------------------------------
'''

class TaskServicesTest(BaseTest):

    def test_task_details(self):
        '''
          Checks if a basic task created with non-optional arguments gives back the expected details.
        '''
        #test task
        task = Task.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)
        owner_prof = Profile.objects.get(user_id=self.user.id)

        test_context = get_task_details(task.id)

        self.assertEqual(test_context["task"].name, task.name)
        self.assertEqual(test_context["proj"], Project.objects.all()[0])
        self.assertEqual(test_context["owner_profile"], owner_prof)

    def test_tasks_for_user(self):
        '''
          Checks for the tasks which were assigned to the specified user.
        '''
        task = Task.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)
        task2 = Task.objects.create(name="test2",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)

        test_tasks = Task.objects.all()

        tasks_for_user = get_tasks_for_user(self.user.id)
        owner_prof = Profile.objects.get(user_id=self.user.id)

        self.assertEqual(tasks_for_user["assigned_tasks"][0],task)
        self.assertEqual(tasks_for_user["assigned_tasks"][1],task2)
        #self.assertQuerysetEqual(tasks_for_user["assigned_tasks"], test_tasks)
        self.assertEqual(tasks_for_user["profile"], owner_prof)

    def test_delete_task(self):
        '''
          Checks if a task was deleted from the database.
        '''
        task = Task.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)

        success = delete_task(task.id)

        self.assertTrue(success)


    def test_change_task_state(self):
        '''
         Checks a full workflow: OPEN->IN PROGRESS->TESTING->DONE->CLOSED->REOPEN->OPEN
        '''
        task = Task.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        ret_value = change_task_state(task.id)

        task = Task.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(task.state, "DONE")

        ret_value = change_task_state(task.id)

        task = Task.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(task.state, "CLOSED")

        ret_value = change_task_state(task.id)

        task = Task.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(task.state, "OPEN")


'''
-----------------------------------------------------------------------------------
Views tests
 - create comment
 - delete comment
 - delete task redirect
 - add worklog
-----------------------------------------------------------------------------------
'''

class TaskViewsTest(BaseTest):

    def test_create_comment_view_redirect(self):
        """
        Tests if the CreateCommentForm gets the input->creates the comment->saves it-> then redirects to the task's detail page.
        """

        task = Task.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        response = self.client.post(reverse('projects:tasks:create_comment',  kwargs={'task_id':task.id}), comment_form, follow=True)
        self.assertRedirects(response,reverse('projects:tasks:detail', kwargs={'task_id':task.id}), status_code=302, target_status_code=200)

    
    def test_create_comment_view_data(self):
        """
          Tests if the created comment's text gets saved for the desired task.
        """
        task = Task.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        self.client.post(reverse('projects:tasks:create_comment',  kwargs={'task_id':task.id}), comment_form, follow=True)

        testcontext = get_task_details(task.id)

        self.assertEqual(testcontext["comments"][0].text, "Hello world!")

    def test_delete_comment_view_redirect(self):
        """
          Tests if the delete_comment view makes the right redirection adn actually deletes the comment.
        """
        task = Task.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        #creating comment
        self.client.post(reverse('projects:tasks:create_comment',  kwargs={'task_id':task.id}), comment_form, follow=True)

        test_comment = get_task_details(task.id)

        #deleting comment
        response = self.client.post(reverse('projects:tasks:delete_comment',  kwargs={'task_id':task.id, 'comment_id':test_comment["comments"][0].id}), follow=True)
        self.assertRedirects(response,reverse('projects:tasks:detail', kwargs={'task_id':task.id}), status_code=302, target_status_code=200)

        #creating another comment to check if only this one exist after the delete
        comment_form2 = {
            "comment_txt": "Hello world again!",
        }

        self.client.post(reverse('projects:tasks:create_comment',  kwargs={'task_id':task.id}), comment_form2, follow=True)

        post_delete_details = get_task_details(task.id)

        self.assertEqual(len(post_delete_details["comments"]), 1)


    def test_delete_task_redirect(self):
        """
         Test the deleting task view.
        """
        task = Task.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        response = self.client.post(reverse('projects:tasks:delete',  kwargs={'task_id':task.id}), follow=True)
        self.assertRedirects(response,reverse('users:index'), status_code=302, target_status_code=200)


    def test_adding_worklog(self):
        """
         Tests the view's redirection and if the worklog is in the database.
        """
        task = Task.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        test_worklog_form = {
            "log_date": datetime.strptime("2020-04-15","%Y-%m-%d").date(),
            "logged_hour": 8
        }

        response = self.client.post(reverse('projects:tasks:add_worklog',  kwargs={'task_id':task.id}), test_worklog_form, follow=True)
        self.assertRedirects(response,reverse('projects:tasks:detail', kwargs={'task_id':task.id}), status_code=302, target_status_code=200)

        test_details = get_task_details(task.id)

        self.assertEqual(test_details["worklogs"][0].logged_hour, 8)
