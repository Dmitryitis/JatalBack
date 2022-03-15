from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create(username='test', email='test', password='test', first_name='test',
                                              last_name='test')
        self.test_user1.save()
        self.test_user2 = User.objects.create(username='test2', email='test2', password='test2', first_name='test2',
                                              last_name='test2')
        self.test_user2.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('main_personal'))
        self.assertRedirects(resp, '/auth/main_auth/?next=/cabinet/cabinet/')

    def test_is_ok_page_login(self):
        response = self.client.get(reverse('auth_jatal'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_is_ok_page_register(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login(self):
        credentials = {
            'username': 'test1',
            'password': 'test1'
        }
        user = User.objects.create_user(**credentials)
        login = self.client.post(reverse('auth_jatal'), credentials, follow=True)
        self.assertTrue(login.context['user'].is_active)

    def test_registration_correct(self):
        data = {
            'username': 'test3',
            'email': 'test3@gmail.com',
            'password': 'test3',
            'rep_password': 'test3',
            'firstname': 'test3',
            'lastname': 'test3'
        }

        response = self.client.post(reverse('registration'), data)
        user = User.objects.get(username=data['username'])

        self.assertIsInstance(user, User)

    def test_logout(self):
        credentials = {
            'username': 'test1',
            'password': 'test1'
        }
        user = User.objects.create_user(**credentials)
        login = self.client.post(reverse('auth_jatal'), credentials, follow=True)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('main_page'))

    def test_main_page_correct(self):
        response = self.client.get(reverse('main_page'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
