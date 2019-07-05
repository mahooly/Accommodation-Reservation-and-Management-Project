from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from accommodation.models import Accommodation
from review.forms import ReviewForm, RatingForm
from review.models import Review


@method_decorator(login_required, name='dispatch')
class CreateReview(View):
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        rating_form = RatingForm(request.POST)
        accommodation_id = kwargs['accid']
        rating = None
        if form.is_valid():
            if rating_form.is_valid():
                rating = rating_form.save()
            accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
            comment = form.save(commit=False)
            comment.accommodation = accommodation
            comment.rating = rating
            comment.user = request.user
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد!')
        else:
            messages.error(request, 'در ثبت نظر شما مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')

        return redirect(reverse('accommodation_detail', kwargs={'pk': accommodation_id}))
