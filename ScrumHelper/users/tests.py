from django.test import TestCase
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render, redirect, reverse

from projects.models import Project
from projects.stories.models import UserStory
from projects.tasks.models import Task
from projects.epics.models import Epic
from projects.issues.models import Issue
from projects.stories.services import get_stories_for_user
from projects.epics.services import get_epics_for_user
from projects.tasks.services import get_tasks_for_user
from projects.issues.services import get_issues_for_user

from users.models import Profile

from worklogs.models import Worklog

class BaseTest(TestCase):
    '''
      Set up test environment: create superuser and log it in.
    '''
    def setUp(self):
        superuser = User.objects.create_superuser(
            'test', 'test@api.com', 'testpassword')
        self.user = superuser
        self.client.login(username=superuser.username, password='testpassword')
    
class UsersViewTest(BaseTest):

    def test_user_details(self):

        project = Project.objects.create(name='Test Project', project_owner=self.user)
        epic = Epic.objects.create(name='testEpic', owner=Profile.objects.get(user_id=self.user.id), project_code=project)
        story = UserStory.objects.create(name='test story', owner=self.user, assignee=self.user, project_code=project, epic=epic)
        task = Task.objects.create(name='test task', owner=self.user, assignee=self.user, project_code=project,epic=epic)
        issue = Issue.objects.create(name='test issue', owner=self.user, assignee=self.user, project_code=project, defect_type='BUG')

        profile = Profile.objects.get(user_id=self.user.id)

        context = get_stories_for_user(self.user.id)

        epics = get_epics_for_user(self.user.id)

        context.update(epics)

        tasks = get_tasks_for_user(self.user.id)

        context.update(tasks)

        issues = get_issues_for_user(self.user.id)

        context.update(issues)

        context['profile'] = profile

        self.assertEqual(context["assigned_stories"][0], story)
        self.assertEqual(context["assigned_issues"][0], issue)
        self.assertEqual(context["assigned_tasks"][0], task)
        self.assertEqual(context["epic_owner"][0], epic)
        self.assertEqual(context["profile"], profile)

    def test_users_worklogs(self):

        project = Project.objects.create(name='Test Project', project_owner=self.user)
        story = UserStory.objects.create(name="test story",project_code=Project.objects.all()[0],owner=self.user)

        test_worklog_form = {
            "log_date": datetime.strptime("2020-04-15","%Y-%m-%d").date(),
            "logged_hour": 8
        }

        self.client.post(reverse('projects:stories:add_worklog',  kwargs={'story_id':story.id}), test_worklog_form, follow=True)

        response = self.client.post(reverse('users:get_users_worklogs', kwargs={'username': self.user.username}), {'month': '2020-04-15'})
        self.assertEqual(response.status_code,200)

    
    def test_delete_worklog_redirect(self):

        project = Project.objects.create(name='Test Project', project_owner=self.user)
        story = UserStory.objects.create(name="test story",project_code=Project.objects.all()[0],owner=self.user)

        test_worklog_form = {
            "log_date": datetime.strptime("2020-04-15","%Y-%m-%d").date(),
            "logged_hour": 8
        }

        self.client.post(reverse('projects:stories:add_worklog',  kwargs={'story_id':story.id}), test_worklog_form, follow=True)

        self.client.post(reverse('users:get_users_worklogs', kwargs={'username': self.user.username}), {'month': '2020-04-15'})

        response = self.client.post(reverse('users:delete_worklog', kwargs={'log_id': Worklog.objects.get(log_date=datetime.strptime("2020-04-15","%Y-%m-%d").date()).id}), follow=True)
        self.assertRedirects(response, reverse('users:get_users_worklogs', kwargs={'username': self.user.username}))

    def test_add_group(self):

        self.client.post(reverse('users:group_list'), {'group': 'devs'})

        self.assertEqual(len(Group.objects.all()),1)
        self.assertEqual(Group.objects.all()[0].name,'devs')

    def test_delete_group(self):

        self.client.post(reverse('users:group_list'), {'group': 'devs'})
        self.client.post(reverse('users:delete_group', kwargs={'gr_id': Group.objects.all()[0].id}))

        self.assertEqual(len(Group.objects.all()),0)

    def test_delete_user(self):

        signup_form = {
            'username': 'tester2',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@api.com',
            'password1': 'testpassword12',
            'password2': 'testpassword12',
            'group': '',
        }
        
        self.client.post(reverse('login:signup'), signup_form, follow=True)
        
        #succesfully aded new user
        self.assertEqual(len(User.objects.all()), 2)

        self.client.post(reverse('users:delete_user', kwargs={'user_id': User.objects.get(username='tester2').id}))
        
        #successfulyl deleted the new user: tester2
        self.assertEqual(len(User.objects.all()), 1)

