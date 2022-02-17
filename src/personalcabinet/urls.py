from django.urls import path, re_path

from personalcabinet.views import write_post, single_post, create_comment, \
    PersonalCabinetUser, PersonalCabinetPosts, my_custom_page_not_found_view

urlpatterns = [
    path('cabinet/', PersonalCabinetUser.as_view(), name='main_personal'),
    path('cabinetposts/', PersonalCabinetPosts.as_view(), name='cabinet_posts'),
    path('writepost/', write_post, name="write_post"),
    re_path(r'singlepost/(?P<post_id>\d+)/', single_post, name='single_post'),
    path('create_comment/<int:post_id>/', create_comment, name='create_comment')
]
