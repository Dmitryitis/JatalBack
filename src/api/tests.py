import json
from datetime import datetime
from unittest import mock
from django.core.files import File

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password

from api.serializers import CommentSerializer, CreateCommentSerializer
from main_pages.models import User
from personalcabinet.models import Post, Topic, Comment

User = get_user_model()


class ApiTests(APITestCase):

    def setUp(self):
        user_test1 = User.objects.create_user(username='Dmitry', email='dmitry@gmail.com',
                                              password=make_password('123'), is_superuser=False, )
        user_test1.save()

        topic_test1 = Topic.objects.create(name='Social')

        img_mock = mock.MagicMock(spec=File)
        img_mock.name = "default.jpg"

        self.post_test1 = Post.objects.create(title='aaaa', text='ddddd', author=user_test1, topic=topic_test1,
                                              photo=img_mock.name)
        self.post_test1.save()

        self.comment_test1 = Comment.objects.create(text='test', author_id=user_test1.id, post_id=self.post_test1.id)
        self.comment_test1.save()

        self.valid_comment = {
            'text': 'test2',
            'author': user_test1.id,
            'post': self.post_test1.id,
            'date_created': str(datetime.now())
        }

        self.valid_comment_update = {
            'text': 'test2',
        }

    def test_get_token(self):
        response = self.client.get(reverse('csrf_token'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comments(self):
        response = self.client.get(reverse('sample-list', kwargs={'post_id': self.post_test1.id}), format='json')
        comments = CommentSerializer(self.comment_test1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], comments)

    def test_fail_get_comments(self):
        response = self.client.get(reverse('sample-list', kwargs={'post_id': 100}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_comment(self):
        response = self.client.post(path=f'/api/{self.post_test1.id}/comment/',
                                    data=json.dumps(self.valid_comment),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_comment(self):
        response = self.client.put(path=f'/api/{self.post_test1.id}/comment/{self.comment_test1.id}',
                                   data=json.dumps(self.valid_comment_update),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_delete_comment(self):
        response = self.client.delete(path=f'/api/{self.post_test1.id}/comment/{self.comment_test1.id}')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
