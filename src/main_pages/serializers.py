from rest_framework.serializers import ModelSerializer

from personalcabinet.models import Post


class PostsSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', ]
