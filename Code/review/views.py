from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from accommodation.decorators import user_same_as_accommodation_user
from accommodation.models import Accommodation
from registration.decorators import user_is_host, user_is_confirmed
from review.forms import ReviewForm, RatingForm, ReplyForm
from review.models import Review


@method_decorator([login_required, user_is_confirmed], name='dispatch')
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


@method_decorator([login_required, user_is_confirmed, user_is_host, user_same_as_accommodation_user], name='dispatch')
class AccommodationReviews(ListView):
    template_name = 'review/accommodation_reviews.html'

    def get_queryset(self):
        acc = self.get_accommodation()
        return Review.objects.filter(accommodation=acc)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        acc = self.get_accommodation()
        context['accommodation'] = acc
        return context

    def get_accommodation(self):
        pk = self.kwargs.get('pk')
        return Accommodation.objects.get(pk=pk)


@method_decorator([login_required, user_is_confirmed, user_is_host, user_same_as_accommodation_user], name='dispatch')
class CreateReply(View):
    def post(self, request, *args, **kwargs):
        form = ReplyForm(request.POST)
        review_id = kwargs['pk']
        review = get_object_or_404(Review, pk=review_id)
        if form.is_valid():
            reply = form.save()
            review.reply = reply
            review.save()
            messages.success(request, 'پاسخ شما با موفقیت ارسال شد!')
        else:
            messages.error(request, 'در ارسال پاسخ شما مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')

        return redirect(reverse('accommodation_review', kwargs={'pk': review.accommodation.id}))
