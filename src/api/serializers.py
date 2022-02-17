from django.contrib.auth.models import User
from rest_framework import serializers

from personalcabinet.models import Comment, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    date_created = serializers.DateTimeField(format='%m %d,%Y %H:%M')
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'date_created', 'post')


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'post', 'date_created', 'author')
