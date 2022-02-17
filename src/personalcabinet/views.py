from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from auth_jatal.models import Profile
from personalcabinet.forms import CreatePost, CreateComment
from personalcabinet.models import Topic, Post, Comment
from personalcabinet.service import get_views, get_filter_f, get_filter_Q


@login_required
def main_personal(request):
    context = {
        'user': request.user
    }
    return render(request, 'personalCabinet.html', context)


class PersonalCabinetUser(DetailView):
    context_object_name = 'user'
    template_name = 'personalCabinet.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PersonalCabinetUser, self).dispatch(request, *args, **kwargs)


@login_required
def cabinet_posts(request):
    posts = Post.objects.filter(author=request.user)
    context = {
        'posts': posts
    }
    return render(request, 'personalAllPost.html', context)


class PersonalCabinetPosts(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'personalAllPost.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PersonalCabinetPosts, self).dispatch(request, *args, **kwargs)


@login_required
def write_post(request):
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            photo = form.cleaned_data['photo']
            text = form.cleaned_data['text']
            agreement = form.cleaned_data['agreement']
            original = form.cleaned_data['original']
            author = request.user
            topic = Topic.objects.get(name=request.POST['topic'])
            print(topic)

            Post.objects.create(title=title, photo=photo, text=text, author=author, topic=topic, agreement=agreement,
                                original=original)
            return redirect('cabinet_posts')

    topics = Topic.objects.all()
    context = {
        'topics': topics
    }
    return render(request, 'writepost.html', context)


def single_post(request, post_id):
    res = get_filter_f()
    print(res)
    res = get_filter_Q()
    print(res)
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post_id)
    view = get_views(post_id)
    view = view.get('id__count')
    if request.user.is_authenticated:
        if request.user not in post.view.all():
            post.view.add(request.user)
        context = {
            'post': post,
            'comments': comments,
            'user': request.user,
            'view': view
        }
        return render(request, 'singlepost.html', context)
    context = {
        'post': post,
        'comments': comments,
        'user': '',
        'view': view
    }
    return render(request, 'singlepost.html', context)


@login_required
def create_comment(request, post_id):
    if request.method == 'POST':
        form = CreateComment(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            Comment.objects.create(text=text, author=request.user, post_id=post_id)
            return redirect('single_post', post_id)


def my_custom_page_not_found_view(request, *args, **kwargs):
    context = {
        'user': request.user
    }
    return render(request, '404_error_page.html', context)
