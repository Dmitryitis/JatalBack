from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from auth_jatal.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('about', 'user', User,)
    search_fields = (User.username,)
    list_filter = ('user', 'about')
