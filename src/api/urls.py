from django.urls import re_path, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import SimpleRouter

from api.views import api_user, get_csrf_token, CommentView

router = SimpleRouter()
router.register(prefix='(?P<post_id>\d+)/comment', viewset=CommentView, basename='sample')

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Api for Jatal",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True
)

urlpatterns = [
    re_path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('user/', api_user, name='api_user'),
    path('get-token/', get_csrf_token, name='csrf_token'),
    *router.urls
]
