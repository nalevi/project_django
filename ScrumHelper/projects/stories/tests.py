from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from datetime import datetime

from projects.forms import CreateStoryForm
from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic
from projects.stories.models import UserStory
from projects.stories.services import get_story_details, get_stories_for_user, delete_story, change_story_state, get_story_object
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

'''
-----------------------------------------------------------------------------------
Services tests
 - get story details
 - get storis for a user
 - delete story
 - change story state
-----------------------------------------------------------------------------------
'''

class StoryServicesTest(BaseTest):

    def test_story_details(self):
        '''
          Checks if a basic story created with non-optional arguments gives back the expected details.
        '''
        #test story
        story = UserStory.objects.create(name="testStory",project_code=Project.objects.all()[0],owner=self.user)
        owner_prof = Profile.objects.get(user_id=self.user.id)

        test_context = get_story_details(story.id)

        self.assertEqual(test_context["story"].name, story.name)
        self.assertEqual(test_context["proj"], Project.objects.all()[0])
        self.assertEqual(test_context["owner_profile"], owner_prof)

    def test_stories_for_user(self):
        '''
          Checks for the stories which were assigned to the specified user.
        '''
        story = UserStory.objects.create(name="testStory",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)
        story2 = UserStory.objects.create(name="testStory2",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)

        test_stories = UserStory.objects.all()

        stories_for_user = get_stories_for_user(self.user.id)
        owner_prof = Profile.objects.get(user_id=self.user.id)

        users_stories = stories_for_user["assigned_stories"].order_by('id')

        self.assertEqual(users_stories[0],story)
        self.assertEqual(users_stories[1],story2)
        #self.assertQuerysetEqual(stories_for_user["assigned_stories"], test_stories)
        self.assertEqual(stories_for_user["profile"], owner_prof)

    def test_delete_story(self):
        '''
          Checks if a story was deleted from the database.
        '''
        story = UserStory.objects.create(name="testStory",project_code=Project.objects.all()[0],owner=self.user, assignee=self.user)

        success = delete_story(story.id)

        self.assertTrue(success)


    def test_change_story_state(self):
        '''
         Checks a full workflow: OPEN->IN PROGRESS->TESTING->DONE->CLOSED->REOPEN->OPEN
        '''
        story = UserStory.objects.create(name="testStory",project_code=Project.objects.all()[0],owner=self.user)

        ret_value = change_story_state(story.id)

        story = UserStory.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(story.state, "IN PROGRESS")

        ret_value = change_story_state(story.id)

        story = UserStory.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(story.state, "TESTING")

        ret_value = change_story_state(story.id)

        story = UserStory.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(story.state, "DONE")

        ret_value = change_story_state(story.id)

        story = UserStory.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(story.state, "CLOSED")

        ret_value = change_story_state(story.id)

        story = UserStory.objects.all()[0]

        self.assertTrue(ret_value)
        self.assertEqual(story.state, "OPEN")


'''
-----------------------------------------------------------------------------------
Views tests
 - create comment
 - delete comment
 - delete story redirect
 - add worklog
-----------------------------------------------------------------------------------
'''

class StoryViewsTest(BaseTest):

    def test_create_comment_view_redirect(self):
        """
        Tests if the CreateCommentForm gets the input->creates the comment->saves it-> then redirects to the story's detail page.
        """

        story = UserStory.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        response = self.client.post(reverse('projects:stories:create_comment',  kwargs={'story_id':story.id}), comment_form, follow=True)
        self.assertRedirects(response,reverse('projects:stories:detail', kwargs={'story_id':story.id}), status_code=302, target_status_code=200)

    
    def test_create_comment_view_data(self):
        """
          Tests if the created comment's text gets saved for the desired story.
        """
        story = UserStory.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        self.client.post(reverse('projects:stories:create_comment',  kwargs={'story_id':story.id}), comment_form, follow=True)

        testcontext = get_story_details(story.id)

        self.assertEqual(testcontext["comments"][0].text, "Hello world!")

    def test_delete_comment_view_redirect(self):
        """
          Tests if the delete_comment view makes the right redirection adn actually deletes the comment.
        """
        story = UserStory.objects.create(name="test",project_code=Project.objects.all()[0],owner=self.user)

        comment_form = {
            "comment_txt": "Hello world!",
        }

        #creating comment
        self.client.post(reverse('projects:stories:create_comment',  kwargs={'story_id':story.id}), comment_form, follow=True)

        test_comment = get_story_details(story.id)

        #deleting comment
        response = self.client.post(reverse('projects:stories:delete_comment',  kwargs={'story_id':story.id, 'comment_id':test_comment["comments"][0].id}), follow=True)
        self.assertRedirects(response,reverse('projects:stories:detail', kwargs={'story_id':story.id}), status_code=302, target_status_code=200)

        #creating another comment to check if only this one exist after the delete
        comment_form2 = {
            "comment_txt": "Hello world again!",
        }

        self.client.post(reverse('projects:stories:create_comment',  kwargs={'story_id':story.id}), comment_form2, follow=True)

        post_delete_details = get_story_details(story.id)

        self.assertEqual(len(post_delete_details["comments"]), 1)


    def test_delete_story_redirect(self):
        """
         Test the deleting story view.
        """
        story = UserStory.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        response = self.client.post(reverse('projects:stories:delete',  kwargs={'story_id':story.id}), follow=True)
        self.assertRedirects(response,reverse('users:index'), status_code=302, target_status_code=200)


    def test_adding_worklog(self):
        """
         Tests the view's redirection and if the worklog is in the database.
        """
        story = UserStory.objects.create(name="name",project_code=Project.objects.all()[0],owner=self.user)

        test_worklog_form = {
            "log_date": datetime.strptime("2020-04-15","%Y-%m-%d").date(),
            "logged_hour": 8
        }

        response = self.client.post(reverse('projects:stories:add_worklog',  kwargs={'story_id':story.id}), test_worklog_form, follow=True)
        self.assertRedirects(response,reverse('projects:stories:detail', kwargs={'story_id':story.id}), status_code=302, target_status_code=200)

        test_details = get_story_details(story.id)

        self.assertEqual(test_details["worklogs"][0].logged_hour, 8)
