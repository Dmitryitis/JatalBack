import PIL
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from PIL import Image

user = get_user_model()


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='заголовок')
    photo = models.ImageField(upload_to='images/', verbose_name='фото')
    text = models.TextField(verbose_name='текст')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='топик')
    author = models.ForeignKey(user, on_delete=models.CASCADE, verbose_name='автор')
    date_create = models.DateTimeField(auto_now=True, db_index=True, verbose_name='дата создания')
    view = models.ManyToManyField(user, related_name='view')
    agreement = models.BooleanField(verbose_name='соглашение', null=True)
    original = models.BooleanField(verbose_name='оригинал текста', null=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.title}'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.photo.path)
        img.resize((1920, 1280), PIL.Image.ANTIALIAS)
        img.save(self.photo.path, format='JPEG', quality=85, progressive=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    text = models.TextField(verbose_name='комментарий')
    date_created = models.DateTimeField(auto_now=True, db_index=True, verbose_name='дата создания')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
