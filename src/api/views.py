from django.http import JsonResponse
from django.middleware.csrf import get_token
# Create your views here.
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import CommentSerializer, UserSerializer, CreateCommentSerializer
from personalcabinet.models import Comment


class AuthenticatedPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return True


@swagger_auto_schema(
    method='get',
    request_body=no_body,
    operation_summary='Authorized user',
    responses={200: 'success'}
)
@api_view(['GET'])
@permission_classes((AuthenticatedPermissions,))
def api_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    return Response(status=404, data='No authenticated')


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'token': token,
                         'status': 200})


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, post_id=None, *args, **kwargs):
        comments = Comment.objects.filter(post=post_id).order_by('-date_created')
        if comments:
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        else:
            return Response(status=404, data='Not found')

    def create(self, request, post_id=None, *args, **kwargs):
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data='created')
        return Response(status=403, data='Not valid')

    def destroy(self, request, post_id=None, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=200, data='success')

    def update(self, request, post_id=None, *args, **kwargs):
        comment = self.get_object()
        comment.text = request.data['text']
        comment.save()
        return Response(status='200', data='update')
