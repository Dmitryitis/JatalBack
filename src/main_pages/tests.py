from http import HTTPStatus

from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class MainPagesTests(TestCase):

    def test_all_posts_correct(self):
        response = self.client.get(reverse('all_posts'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'allpost.html')

    def test_about_correct(self):
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about.html')

    def test_contact_correct(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'contact.html')
