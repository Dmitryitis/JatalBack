from django.urls import path

from auth_jatal.views import main_login, auth_jatal, registration, logout_view, main_forgot, send_email, password_reset

urlpatterns = [
    path('main_auth/', main_login, name='main_login'),
    path('auth/', auth_jatal, name='auth_jatal'),
    path('registration/', registration, name='registration'),
    path('logout/', logout_view, name='logout'),
    path('main_forgot/', main_forgot, name='forgot'),
    path('send_email/', send_email, name='send_email'),
    path('password_reset/<int:user_id>/<str:token>', password_reset, name='password_reset')
]
