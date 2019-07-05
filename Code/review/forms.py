from django import forms

from review.models import Review, Rating, Reply


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('accommodation', 'user', 'reply', 'rating', 'helpful_count')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = '__all__'
