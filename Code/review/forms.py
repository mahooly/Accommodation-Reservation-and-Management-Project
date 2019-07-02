from django import forms

from review.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('accommodation', 'user',)