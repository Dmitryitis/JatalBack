from django.contrib.auth import get_user_model
from django.db import models

from personalcabinet.models import Post, Topic

User = get_user_model()


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    class Meta:
        abstract = True


class Journal(BaseModel):
    journal_name = models.CharField(max_length=70, verbose_name='название журнала')
    journal_description = models.TextField(verbose_name='краткое описание')
    journal_href = models.URLField(verbose_name='ссылка на журнал')

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'


class JournalArticle(BaseModel):
    article = models.CharField(max_length=225, verbose_name='название статьи')
    article_description = models.TextField(max_length=255, verbose_name='краткое описание')
    author_name = models.CharField(max_length=80, verbose_name='автор статьи')
    journal_id = models.ForeignKey(Journal, on_delete=models.CASCADE, verbose_name='журнал')
    article_href = models.URLField(verbose_name='ссылка на статью')

    class Meta:
        verbose_name = 'Статья журнала'
        verbose_name_plural = 'Статьи журнала'


class Community(BaseModel):
    community_name = models.CharField(max_length=255, verbose_name='название сообщества')
    community_description = models.TextField(max_length=255, verbose_name='краткое описание')
    img = models.ImageField(upload_to='images/', verbose_name='фото сообщества')
    community_topics = models.ManyToManyField(Topic, related_name='com_topic')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'


class CommunityMember(BaseModel):
    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='участник сообщества')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name='сообщество')
    is_support = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Участник сообщеста'
        verbose_name_plural = 'Участники сообщества'


class CommunityPost(BaseModel):
    community_author = models.ForeignKey(CommunityMember, on_delete=models.CASCADE, verbose_name='автор')
    community_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name='статья сообщества')
    community_article = models.ForeignKey(JournalArticle, on_delete=models.CASCADE, verbose_name='статья из журнала',
                                          null=True, blank=True)
    community_post_views = models.ManyToManyField(User, related_name='com_post_views')
    community_post_likes = models.ManyToManyField(User, related_name='com_post_likes')

    class Meta:
        verbose_name = 'Пост сообщества'
        verbose_name_plural = 'Посты сообщества'


class CommunityPostComment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор комментария')
    community_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост сообщества')
    comment_text = models.TextField(verbose_name='текст комментария')

    class Meta:
        verbose_name = 'Комментарий поста сообщества'
        verbose_name_plural = 'Комментарии поста сообщества'


class Company(BaseModel):
    company_name = models.CharField(max_length=120, verbose_name='название компании')
    company_logo = models.ImageField(upload_to='images/', verbose_name='фото компании')
    company_description = models.TextField(max_length=255, verbose_name='краткое описание')
    company_members = models.ManyToManyField(User, related_name='company_members')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='админ компании')
    company_href = models.URLField(max_length=120, verbose_name='ссылка на компанию')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class CompanyPost(BaseModel):
    company_article_link = models.URLField(max_length=255, verbose_name='ссылка на статью')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='компания')

    class Meta:
        verbose_name = 'Пост компании'
        verbose_name_plural = 'Посты компании'
