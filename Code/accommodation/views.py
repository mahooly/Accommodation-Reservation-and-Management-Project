from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView

from Code.settings import DEFAULT_FROM_EMAIL
from .forms import AccommodationCreationForm, AmenityForm, RoomCreationForm, AccommodationChangeForm, FileFieldForm, \
    RoomSearchForm
from .models import Accommodation, Amenity, Image, RoomInfo, Room
from registration.decorators import user_is_host
from .decorators import user_same_as_accommodation_user, user_host_or_superuser, user_same_as_image_user
from datetime import timedelta
from django.db.models import Q
import datetime


@method_decorator([login_required, user_is_host], name='dispatch')
class CreateAccommodationView(View):
    template_name = 'accommodation/create_accommodation.html'

    def get(self, request, *args, **kwargs):
        form = AccommodationCreationForm()
        image_form = FileFieldForm()
        return render(request, self.template_name,
                      {'form': form, 'image_form': image_form})

    def post(self, request, *args, **kwargs):
        form = AccommodationCreationForm(request.POST)
        image_form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            owner = request.user.host
            house = form.save(commit=False)
            house.owner = owner
            house.save()
            form.save_m2m()
            files = request.FILES.getlist('image')
            for f in files:
                Image.objects.create(accommodation=house, image=f)
            messages.success(request, 'اقامتگاه با موفقیت ایجاد شد.')
            url = '/accommodation/' + str(house.pk)
            return redirect(url)
        else:
            return render(request, self.template_name,
                          {'form': form, 'image_form': image_form})


class AccommodationDetailView(DetailView):
    model = Accommodation
    format = '%m/%d/%Y'
    template_name = 'accommodation/accommodation_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RoomCreationForm()
        context['form'] = form

        pk = self.kwargs.get('pk')
        rooms = Room.objects.filter(accommodation__id__exact=pk)
        form = RoomSearchForm(self.request.GET)
        stay_length = 0
        rooms_fat = {}
        for r in list(rooms):
            rooms_fat[r] = range(r.how_many)

        if form.is_valid():
            check_in = form.cleaned_data.get('check_in', '')
            check_out = form.cleaned_data.get('check_out', '')
            context['check_in'] = check_in
            context['check_out'] = check_out
            price = form.cleaned_data.get('price', '')

            if check_in:
                check_in = self.convert_string_to_date(check_in)
                check_out = self.convert_string_to_date(check_out)

                availableRoomInfos1 = RoomInfo.objects.all().exclude(
                    Q(reservation__check_in__range=(check_in, check_out - timedelta(days=1))),
                    Q(reservation__is_canceled=False))
                availableRoomInfos2 = availableRoomInfos1.exclude(
                    Q(reservation__check_out__range=(check_in + timedelta(days=1), check_out)),
                    Q(reservation__is_canceled=False))
                availableRoomInfos = availableRoomInfos2.filter(out_of_service=False)
                rooms = rooms.filter(roominfo__in=availableRoomInfos)
                for r in list(rooms):
                    rooms_fat[r] = range(list(rooms).count(r))
                rooms = rooms.distinct()
                stay_length = (check_out - check_in).days

            if price:
                price_low = int(price.split('-')[0]) * 1000
                price_high = int(price.split('-')[1]) * 1000
                if price_high == 900 * 1000:
                    rooms = rooms.filter(price__gte=price_low)
                else:
                    rooms = rooms.filter(price__gte=price_low, price__lte=price_high)

        context['rooms'] = rooms
        context['stay_length'] = stay_length
        context['room_count'] = rooms_fat
        return context

    def convert_string_to_date(self, date_string):
        return datetime.datetime.strptime(date_string, self.format)

    def convert_date_to_string(self, datetime_object):
        return datetime_object.strftime(self.format)

    def convert_date_to_string_2(self, datetime_object):
        format2 = '%Y-%m-%d'
        return datetime_object.strftime(format2)


@method_decorator([login_required, user_is_host, user_same_as_accommodation_user], name='dispatch')
class CreateRoomView(View):
    def post(self, request, *args, **kwargs):
        form = RoomCreationForm(request.POST, request.FILES)
        accommodation_id = kwargs['accid']
        if form.is_valid():
            accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
            room = form.save(commit=False)
            room.accommodation = accommodation
            room.save()
            form.save_m2m()
            how_many = form.cleaned_data.get('how_many')
            for i in range(how_many):
                RoomInfo.objects.create(room=room)
            messages.success(request, 'اتاق با موفقیت اضافه شد.')
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)
        else:
            messages.error(request, 'در اضافه کردن اتاق مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)


@method_decorator([login_required, user_host_or_superuser], name='dispatch')
class DeleteAccommodation(View):
    def get(self, request, *args, **kwargs):
        acc_pk = kwargs['pk']
        acc = get_object_or_404(Accommodation, pk=acc_pk)
        send_mail(
            'حذف محل اقامت',
            'محل اقامت شما حذف شده است.',
            DEFAULT_FROM_EMAIL,
            [acc.email],
            fail_silently=False,
        )
        acc.delete()
        messages.success(request, 'اقامتگاه با موفقیت حذف شد.')
        if request.user.is_host:
            return redirect('/host_dashboard')
        else:
            return redirect('/admin_dashboard/accommodations')


@method_decorator([login_required, user_is_host, user_same_as_accommodation_user], name='dispatch')
class EditAccommodation(View):
    template_name = 'accommodation/edit_accommodation.html'

    def get(self, request, *args, **kwargs):
        accommodation_id = kwargs['pk']
        images = Image.objects.filter(accommodation_id=accommodation_id)
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        amenity = [obj.pk for obj in accommodation.amenity.all()]
        amenities = Amenity.objects.all()
        form = AccommodationChangeForm(instance=accommodation,
                                       initial={'title': accommodation.title,
                                                'accommodation_type': accommodation.accommodation_type,
                                                'description': accommodation.description,
                                                'address': accommodation.address, 'email': accommodation.email,
                                                'phone': accommodation.phone,
                                                'city': accommodation.city,
                                                'province': accommodation.province,
                                                'images': images,
                                                'amenity': amenity})
        image_form = FileFieldForm()
        return render(request, self.template_name,
                      {'form': form, 'image_form': image_form, 'amenities': amenities})

    def post(self, request, *args, **kwargs):
        accommodation_id = kwargs['pk']
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        images = Image.objects.filter(accommodation_id=accommodation_id)
        form = AccommodationChangeForm(request.POST, request.FILES, instance=accommodation)
        image_form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات شما با موفقیت ثبت شد.')
            files = request.FILES.getlist('image')
            for f in files:
                Image.objects.create(accommodation=accommodation, image=f)
        amenity = [obj.pk for obj in accommodation.amenity.all()]
        amenities = Amenity.objects.all()
        form = AccommodationChangeForm(instance=accommodation,
                                       initial={'title': accommodation.title,
                                                'accommodation_type': accommodation.accommodation_type,
                                                'description': accommodation.description,
                                                'address': accommodation.address, 'email': accommodation.email,
                                                'phone': accommodation.phone,
                                                'city': accommodation.city,
                                                'province': accommodation.province,
                                                'images': images,
                                                'amenity': amenity})
        image_form = FileFieldForm()
        return render(request, self.template_name,
                      {'form': form, 'image_form': image_form, 'amenities': amenities})


@method_decorator([login_required, user_is_host, user_same_as_image_user], name='dispatch')
class DeleteImage(View):
    def get(self, request, *args, **kwargs):
        img_pk = kwargs['pk']
        img = get_object_or_404(Image, pk=img_pk)
        accommodation = img.accommodation
        img.delete()
        url = '/edit_accommodation/' + str(accommodation.pk)
        messages.success(request, 'عکس با موفقیت حذف شد.')
        return redirect(url)


@method_decorator([login_required, user_is_host], name='dispatch')
class CreateAmenityView(View):
    def post(self, request, *args, **kwargs):
        form = AmenityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'امکانات با موفقیت اضافه شد.')
        else:
            messages.error(request, 'در اضافه کردن امکانات مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')
        return redirect('/create_accommodation/')
