from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Group

from login.forms import SignUpForm

class LoginTest(TestCase):

    def test_user_login(self):

        superuser = User.objects.create_superuser(
            'test', 'test@api.com', 'testpassword')
        self.user = superuser
        #self.client.login(username=superuser.username, password='testpassword')

        response = self.client.post('', {'username':superuser.username, 'password':'testpassword'}, follow=True)
        
        self.assertRedirects(response,'/users/', status_code=302, target_status_code=200)

    def test_user_logout(self):

        superuser = User.objects.create_superuser(
            'test', 'test@api.com', 'testpassword')
        self.user = superuser
        self.client.login(username=superuser.username, password='testpassword')

        response = self.client.post(reverse('login:logout'), follow=True)
        
        self.assertRedirects(response,reverse('login:login'))

    def test_user_signup_form_is_valid(self):

        signup_form = {
            'username': 'tester1',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@api.com',
            'password1': 'testpassword12',
            'password2': 'testpassword12',
        }

        form = SignUpForm(data=signup_form)
        self.assertTrue(form.is_valid())
        

    def test_signup_form_invalid(self):

        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_signup_form_adds_user(self):

        signup_form = {
            'username': 'tester1',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@api.com',
            'password1': 'testpassword12',
            'password2': 'testpassword12',
        }
        
        form = SignUpForm(data=signup_form)
        self.assertTrue(form.is_valid())
        self.client.post(reverse('login:signup'), signup_form, follow=True)
        

        self.assertEqual(len(User.objects.all()), 1) 

    def test_edit_user_form_redirect(self):
        '''
          Tests if the edit form changes the last_name
        '''

        signup_form = {
            'username': 'tester1',
            'first_name': 'Test',
            'last_name': 'Tester',
            'email': 'test@api.com',
            'password1': 'testpassword12',
            'password2': 'testpassword12',
        }
        
        self.client.post(reverse('login:signup'), signup_form, follow=True)


        response = self.client.post(reverse('login:edit_user', kwargs={'user_id': User.objects.all()[0].id}), signup_form, follow=True)

        self.assertRedirects(response, reverse('users:index'))