from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from main_pages.models import Journal, JournalArticle, Community, CommunityMember, Company, CommunityPost, CompanyPost, \
    CommunityPostComment
from personalcabinet.models import Topic, Post, Comment


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

    list_filter = ('name',)
    ordering = ('name', 'id',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'date_create',)
    list_filter = ('author', 'date_create')
    ordering = ('author', 'date_create')
    search_fields = (User.username,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date_created')

    list_filter = ('author', 'post', 'date_created')
    ordering = ('author', 'date_created')


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('journal_name', 'journal_href')
    list_filter = ('journal_name',)
    ordering = ('journal_name', 'created_at')


@admin.register(JournalArticle)
class JournalArticleAdmin(admin.ModelAdmin):
    list_display = ('article', 'article_href')
    list_filter = ('article',)
    ordering = ('article', 'created_at')


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('community_name',)


@admin.register(CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'admin', 'company_href')
    list_filter = ('company_name',)
    ordering = ('company_name', 'created_at')


@admin.register(CommunityPostComment)
class CommunityPostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyPost)
class CompanyPostAdmin(admin.ModelAdmin):
    pass
