from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from personalcabinet.models import Topic, Post

User = get_user_model()


# Create your tests here.
class PersonalCabinetTests(TestCase):

    def setUp(self):
        user_test1 = User.objects.create_user(username='Dmitry', email='dmitry@gmail.com',
                                              password=make_password('123'), is_superuser=False, )
        user_test1.save()

        topic_test1 = Topic.objects.create(name='Social')

        self.post_test1 = Post.objects.create(title='aaaa', text='ddddd', author=user_test1, topic=topic_test1,
                                              photo='images/ph1_IQQJS1D.jpg')
        self.post_test1.save()

    def test_main_personal_page(self):
        credentials = {
            'username': 'test1',
            'password': 'test1'
        }
        user = User.objects.create_user(**credentials)
        login = self.client.post(reverse('auth_jatal'), credentials, follow=True)

        response = self.client.get(reverse('main_personal'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'personalCabinet.html')

    def test_cabinet_posts_page(self):
        credentials = {
            'username': 'test1',
            'password': 'test1'
        }
        user = User.objects.create_user(**credentials)
        login = self.client.post(reverse('auth_jatal'), credentials, follow=True)

        response = self.client.get(reverse('cabinet_posts'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'personalAllPost.html')

    def test_create_post(self):
        credentials = {
            'username': 'test1',
            'password': 'test1'
        }
        user = User.objects.create_user(**credentials)
        topic = Topic.objects.create(name='sport')
        login = self.client.post(reverse('auth_jatal'), credentials, follow=True)

        data = {
            'title': 'tessst',
            'photo': '/images/cyber_TVDg6FA.jpg',
            'text': 'text',
            'agreement': True,
            'original': True,
            'author': user,
            'topic': topic
        }

        response = self.client.post(reverse('write_post'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK)