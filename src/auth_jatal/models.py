from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

user = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    about = models.TextField(null=True, verbose_name='about')

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
