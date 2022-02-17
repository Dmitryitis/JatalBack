from django import forms

from personalcabinet.models import Post, Comment


class CreatePost(forms.ModelForm):
    agreement = forms.BooleanField()
    original = forms.BooleanField()

    class Meta:
        model = Post
        fields = ('title', 'photo', 'text',)


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
