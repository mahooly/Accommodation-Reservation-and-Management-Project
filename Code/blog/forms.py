from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Post, Comment


class BlogCreationForm(forms.ModelForm):
    description = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Post
        fields = ['title', 'description', 'province', 'city', 'image']


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class BlogSearchForm(forms.Form):
    makan = forms.CharField(required=False)
    keyword = forms.CharField(required=False)