from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from datetime import datetime

from projects.forms import CreateIssueForm
from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic
from projects.issues.models import Issue
from projects.issues.services import get_issue_details, get_issues_for_user, delete_issue, change_issue_state, get_issue_object
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

class IssueCreateFormTest(BaseTest):

    def test_create_issue_form_is_valid(self):
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
            'defect_type': 'BUG',
            'solution': None,
            }
        form = CreateIssueForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_issue_form_invalid(self):
        '''
        The UserStoy creating view function's test with invalid form data
        '''
        form = CreateIssueForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

class IssueEditFormTest(BaseTest):

    def test_edit_form_valid_redirect(self):
        '''
        Checks if the editing form redirects to the desired url
        '''

        issue = Issue.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0].pk,
            'assignee': '',
            'description': 'Description',
            'importance':'low',
            'epic': '',
            'defect_type': 'BUG',
            'solution': '',
        }
        response = self.client.post(reverse('projects:issues:issue_edit',  kwargs={'issue_id':issue.id}), form_data, follow=True)
        
        self.assertRedirects(response,reverse('projects:issues:detail', kwargs={'issue_id':issue.id}), status_code=302, target_status_code=200)


    def test_edit_form_invalid_redirect(self):
        '''
        Checks if the editing form is invalid
        '''

        issue = Issue.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        form_data = {
            'name':'New',
            'project_code':Project.objects.all()[0],
            'assignee': '',
            'description': 'Description',
            'importance':'low',
            'epic': '',
        }
        response = self.client.post(reverse('projects:issues:issue_edit',  kwargs={'issue_id':issue.id}), form_data, follow=True)
        self.assertEqual(response.status_code, 200)

'''
-----------------------------------------------------------------------------------
Services tests
 - get issue details
 - get storis for a user
 - delete issue
 - change issue state
-----------------------------------------------------------------------------------
'''

class IssueServicesTest(BaseTest):

    def test_issue_details(self):
        '''
          Checks if a basic issue created with non-optional arguments gives back the expected details.
        '''
        #test issue
        issue = Issue.objects.create(name="testissue",project_code=Project.objects.all()[0],owner=self.user)
        owner_prof = Profile.objects.get(user_id=self.user.id)

        test_context = get_issue_details(issue.id)

        self.assertEqual(test_context["issue"].name, issue.name)
        self.assertEqual(test_context["proj"], Project.objects.all()[0])
        self.assertEqual(test_context["owner_profile"], owner_prof)

    def test_issues_for_user(self):
        '''
          Checks for the issues which were assigned to the specified user.
        '''
        issue = Issue.objects.create(name="testissue",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)
        issue2 = Issue.objects.create(name="testissue2",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)

        test_issues = Issue.objects.all()

        issues_for_user = get_issues_for_user(self.user.id)
        owner_prof = Profile.objects.get(user_id=self.user.id)

        self.assertEqual(issues_for_user["assigned_issues"][0],issue)
        self.assertEqual(issues_for_user["assigned_issues"][1],issue2)
        #self.assertQuerysetEqual(issues_for_user["assigned_issues"], test_issues)
        self.assertEqual(issues_for_user["profile"], owner_prof)

    def test_delete_issue(self):
        '''
          Checks if a issue was deleted from the database.
        '''
        issue = Issue.objects.create(name="testissue",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)

        success = delete_issue(issue.id)

        self.assertTrue(success)


    def test_change_issue_state(self):
        '''
         Checks a full workflow: OPEN->IN PROGRESS->TESTING->DONE->CLOSED->REOPEN->OPEN
        '''
        issue = Issue.objects.create(name="testissue",project_code=Project.objects.all()[0],owner=self.user)

        ret_value = change_issue_state(issue.id)

        issue = Issue.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(issue.state, "IN PROGRESS")

        ret_value = change_issue_state(issue.id)

        issue = Issue.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(issue.state, "TESTING")

        ret_value = change_issue_state(issue.id)

        issue = Issue.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(issue.state, "DONE")

        ret_value = change_issue_state(issue.id)

        issue = Issue.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(issue.state, "CLOSED")

        ret_value = change_issue_state(issue.id)

        issue = Issue.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(issue.state, "OPEN")


'''
-----------------------------------------------------------------------------------
Views tests
 - create comment
 - delete comment
 - delete issue redirect
 - add worklog
-----------------------------------------------------------------------------------
'''

class IssueViewsTest(BaseTest):

    def test_create_comment_view_redirect(self):
        """
        Tests if the CreateCommentForm gets the input->creates the comment->saves it-> then redirects to the issue's detail page.
        """

        issue = Issue.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        response = self.client.post(reverse('projects:issues:create_comment',  kwargs={'issue_id':issue.id}), comment_form, follow=True)
        self.assertRedirects(response,reverse('projects:issues:detail', kwargs={'issue_id':issue.id}), status_code=302, target_status_code=200)

    
    def test_create_comment_view_data(self):
        """
          Tests if the created comment's text gets saved for the desired issue.
        """
        issue = Issue.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        self.client.post(reverse('projects:issues:create_comment',  kwargs={'issue_id':issue.id}), comment_form, follow=True)

        testcontext = get_issue_details(issue.id)

        self.assertEqual(testcontext["comments"][0].text, "Hello world!")

    def test_delete_comment_view_redirect(self):
        """
          Tests if the delete_comment view makes the right redirection adn actually deletes the comment.
        """
        issue = Issue.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        #creating comment
        self.client.post(reverse('projects:issues:create_comment',  kwargs={'issue_id':issue.id}), comment_form, follow=True)

        test_comment = get_issue_details(issue.id)

        #deleting comment
        response = self.client.post(reverse('projects:issues:delete_comment',  kwargs={'issue_id':issue.id, 'comment_id':test_comment["comments"][0].id}), follow=True)
        self.assertRedirects(response,reverse('projects:issues:detail', kwargs={'issue_id':issue.id}), status_code=302, target_status_code=200)

        #creating another comment to check if only this one exist after the delete
        comment_form2 = {
            "comment_txt": "Hello world again!",
        }

        self.client.post(reverse('projects:issues:create_comment',  kwargs={'issue_id':issue.id}), comment_form2, follow=True)

        post_delete_details = get_issue_details(issue.id)

        self.assertEqual(len(post_delete_details["comments"]), 1)


    def test_delete_issue_redirect(self):
        """
         Test the deleting issue view.
        """
        issue = Issue.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        response = self.client.post(reverse('projects:issues:delete',  kwargs={'issue_id':issue.id}), follow=True)
        self.assertRedirects(response,reverse('users:index'), status_code=302, target_status_code=200)


    def test_adding_worklog(self):
        """
         Tests the view's redirection and if the worklog is in the database.
        """
        issue = Issue.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        test_worklog_form = {
            "log_date": datetime.strptime("2020-04-15","%Y-%m-%d").date(),
            "logged_hour": 8
        }

        response = self.client.post(reverse('projects:issues:add_worklog',  kwargs={'issue_id':issue.id}), test_worklog_form, follow=True)
        self.assertRedirects(response,reverse('projects:issues:detail', kwargs={'issue_id':issue.id}), status_code=302, target_status_code=200)

        test_details = get_issue_details(issue.id)

        self.assertEqual(test_details["worklogs"][0].logged_hour, 8)

