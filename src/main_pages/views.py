from django.shortcuts import render
from django.core import serializers

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from main_pages.serializers import PostsSerializer
from personalcabinet.models import Post, Topic
from personalcabinet.service import method_prefetch, method_values


class PostsView(ModelViewSet):
    queryset = Post.objects.all().order_by('-date_create')
    serializer_class = PostsSerializer


def all_posts(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        print(request.POST)
        topic = Topic.objects.filter(name=request.POST['val'])

        search = request.POST['search']
        if len(topic) != 0 and search != '':
            posts = Post.objects.filter(title=search, topic=topic[0].pk)
            shortener_text(posts, 60)
            if request.user.is_authenticated:
                context = {
                    'posts': posts,
                    'topics': topics,
                    'user': request.user
                }
            else:
                context = {
                    'posts': posts,
                    'topics': topics,
                    'user': ''
                }
            return render(request, 'allpost.html', context)
        elif search != '':
            posts = Post.objects.filter(title=search)
            shortener_text(posts, 60)
            if request.user.is_authenticated:
                context = {
                    'posts': posts,
                    'topics': topics,
                    'user': request.user
                }
            else:
                context = {
                    'posts': posts,
                    'topics': topics,
                    'user': ''
                }
            return render(request, 'allpost.html', context)
        elif len(topic) != 0:
            posts = Post.objects.filter(topic=topic[0].pk)
            shortener_text(posts, 60)
            if request.user.is_authenticated:
                context = {
                    'posts': posts,
                    'topics': topics,
                    'user': request.user
                }
            else:
                context = {
                    'posts': posts,
                    'topics': topics,
                    'user': ''
                }
            return render(request, 'allpost.html', context)
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-date_create')
        shortener_text(posts, 60)
        context = {
            'posts': posts,
            'topics': topics,
            'user': request.user
        }
        return render(request, 'allpost.html', context)
    posts = method_prefetch()
    method_values()
    shortener_text(posts, 60)
    context = {
        'posts': posts,
        'topics': topics,
        'user': ''
    }
    return render(request, 'allpost.html', context)


def about(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        return render(request, 'about.html', context)
    return render(request, 'about.html', {'user': ''})


def contact(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        return render(request, 'contact.html', context)
    return render(request, 'contact.html', {'user': ''})


def shortener_text(posts, number):
    for post in posts:
        words = post.text.split(" ")
        if len(words) > number:
            post.text = ''
            for word in range(number):
                post.text += words[word] + ' '
        post.text += '....'
