from django.forms import ModelForm, widgets
from .models import Post, Comment


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ('topic', 'text', 'photo')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        widgets = {'text': widgets.Textarea(attrs={'placeholder': 'Write your comment...'})}
