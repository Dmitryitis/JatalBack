from django.db.models import F, Count, Q

from personalcabinet.models import Post


def get_filter_f():
    return Post.objects.filter(id__gt=F('view')).aggregate(Count('id'))


def get_filter_Q():
    return Post.objects.filter(Q(text__startswith='MySQL') | Q(title__startswith='Новый'))


def get_views(id):
    return Post.objects.get(pk=id).view.aggregate(Count('id'))


def method_prefetch():
    topics = []
    for topic in Post.objects.prefetch_related("topic").all():
        topics.append(topic)
    return topics


def method_values():
    movie_list = Post.objects.values_list('id', 'title')
    print(movie_list)
