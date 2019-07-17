import json
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from khayyam import JalaliDate

from Code.settings import DEFAULT_FROM_EMAIL
from reservation.models import Reservation
from .forms import AccommodationCreationForm, AmenityForm, RoomCreationForm, AccommodationChangeForm, FileFieldForm, \
    RoomSearchForm, RoomInfoForm
from .models import Accommodation, Amenity, Image, RoomInfo, Room, TouristAttraction, RoomOutOfService
from registration.decorators import user_is_host, user_is_confirmed
from .decorators import user_same_as_accommodation_user, user_host_or_superuser, user_same_as_image_user
from datetime import timedelta, date
from django.db.models import Q

persian_numbers = '۱۲۳۴۵۶۷۸۹۰'
english_numbers = '1234567890'
trans_num = str.maketrans(persian_numbers, english_numbers)


@method_decorator([login_required, user_is_confirmed, user_is_host], name='dispatch')
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
            house.latitude = float(form.cleaned_data['lat'])
            house.longitude = float(form.cleaned_data['long'])
            house.save()
            form.save_m2m()
            files = request.FILES.getlist('image')
            for f in files:
                Image.objects.create(accommodation=house, image=f)
            messages.success(request, 'اقامتگاه با موفقیت ایجاد شد.')
            return redirect(reverse('room_list', kwargs={'pk': house.pk}))
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
        attractions = self.get_tourist_json(TouristAttraction.objects.all())
        pk = self.kwargs.get('pk')
        rooms = Room.objects.filter(accommodation__id__exact=pk)
        form = RoomSearchForm(self.request.GET)
        stay_length = 0
        rooms_count = {}
        for r in list(rooms):
            rooms_count[r] = range(1, r.how_many + 1)

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
                availableRoomInfos = availableRoomInfos2.exclude(
                    Q(roomoutofservice__from_date__range=(check_in, check_out - timedelta(days=1))),
                    Q(roomoutofservice__to_date__range=(check_in + timedelta(days=1), check_out)))
                rooms = rooms.filter(roominfo__in=availableRoomInfos)
                for r in list(rooms):
                    rooms_count[r] = range(1, list(rooms).count(r) + 1)
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
        context['room_count'] = rooms_count
        context['attractions'] = attractions
        return context

    def convert_string_to_date(self, date_string):
        split_string = [int(x.translate(trans_num)) for x in date_string.split('/')]
        return JalaliDate(split_string[0], split_string[1], split_string[2]).todate()

    def get_tourist_json(self, attractions):
        features = []
        for attraction in attractions:
            features.append(
                {'type': 'Feature', 'properties': {'icon': attraction.get_attraction_type_display(),
                                                   'description': '<strong class="map-popup-title">{}</strong>{}'.format(
                                                       attraction.name,
                                                       attraction.description)},
                 'geometry': {'type': 'Point',
                              'coordinates': [float(attraction.longitude), float(attraction.latitude)]}})
        return json.dumps(features)


@method_decorator([login_required, user_is_confirmed, user_is_host, user_same_as_accommodation_user], name='dispatch')
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


@method_decorator([login_required, user_is_confirmed, user_host_or_superuser], name='dispatch')
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


@method_decorator([login_required, user_is_confirmed, user_is_host, user_same_as_accommodation_user], name='dispatch')
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


@method_decorator([login_required, user_is_confirmed, user_is_host, user_same_as_image_user], name='dispatch')
class DeleteImage(View):
    def get(self, request, *args, **kwargs):
        img_pk = kwargs['pk']
        img = get_object_or_404(Image, pk=img_pk)
        accommodation = img.accommodation
        img.delete()
        url = '/edit_accommodation/' + str(accommodation.pk)
        messages.success(request, 'عکس با موفقیت حذف شد.')
        return redirect(url)


@method_decorator([login_required, user_is_confirmed, user_is_host], name='dispatch')
class CreateAmenityView(View):
    def post(self, request, *args, **kwargs):
        form = AmenityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'امکانات با موفقیت اضافه شد.')
        else:
            messages.error(request, 'در اضافه کردن امکانات مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')
        return redirect('/create_accommodation/')


class RoomListView(ListView):
    template_name = 'accommodation/room_list.html'

    def get_queryset(self):
        return Room.objects.filter(accommodation__id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        accommodation = get_object_or_404(Accommodation, pk=self.kwargs['pk'])
        context['accommodation'] = accommodation
        form = RoomCreationForm()
        context['form'] = form
        return context


class DeleteRoomView(View):
    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['pk'])
        accommodation = room.accommodation
        room.delete()
        messages.success(request, 'اتاق با موفقیت حذف شد.')
        return redirect(reverse('room_list', kwargs={'pk': accommodation.pk}))


class CreateRoomInfo(View):
    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['pk'])
        form = RoomInfoForm(request.POST)
        if form.is_valid():
            room_info = form.save(commit=False)
            room_info.room = room
            room_info.save()
            messages.success(request, 'اتاق با موفقیت اضافه شد.')
        else:
            messages.success(request, 'در ایجاد اتاق مشکلی پیش آمده است. لطفا دوباره تلاش کنید.')
        return redirect(reverse('room_list', kwargs={'pk': room.accommodation.pk}))


class ChangeRoomInfoView(View):
    def post(self, request, *args, **kwargs):
        room_info = get_object_or_404(RoomInfo, pk=kwargs['pk'])
        form = RoomInfoForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            room_info.number = number
            room_info.save()
            messages.success(request, 'اتاق با موفقیت تغییر کرد.')
        else:
            messages.success(request, 'در تغییر اتاق مشکلی پیش آمده است. لطفا دوباره تلاش کنید.')
        return redirect(reverse('room_list', kwargs={'pk': room_info.room.accommodation.pk}))


class DeleteRoomInfoView(View):
    def get(self, request, *args, **kwargs):
        room_info = get_object_or_404(RoomInfo, pk=kwargs['pk'])
        accommodation = room_info.room.accommodation
        room_info.delete()
        messages.success(request, 'اتاق با موفقیت حذف شد.')
        return redirect(reverse('room_list', kwargs={'pk': accommodation.pk}))


class RoomInfoStatsView(ListView):
    template_name = 'accommodation/room.html'

    def get_queryset(self):
        return Room.objects.filter(accommodation__id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RoomInfoStatsView, self).get_context_data(**kwargs)
        accommodation = get_object_or_404(Accommodation, pk=self.kwargs['pk'])
        context['accommodation'] = accommodation
        from_date = self.request.GET.get('from_date', '')
        to_date = self.request.GET.get('to_date', '')
        room_number = self.request.GET.get('room_number', '')
        room_report = {}
        service_report = {}
        if room_number:
            room_report = Reservation.objects.filter(roominfo__number=room_number)
            service_report = RoomOutOfService.objects.filter(room_info__number=room_number)
        if from_date:
            from_date = self.convert_string_to_date(from_date)
            room_report = room_report.filter(
                Q(check_in__gt=from_date) |
                Q(check_out__gt=from_date))
            service_report = service_report.filter(Q(from_date__gt=from_date) |
                                                   Q(to_date__gt=from_date))
        if to_date:
            to_date = self.convert_string_to_date(to_date)
            room_report = room_report.filter(Q(check_in__lt=to_date) |
                                             Q(check_out__lt=to_date))
            service_report = service_report.filter(Q(from_date__lt=to_date) |
                                                   Q(to_date__lt=to_date))
        report = list(chain(room_report, service_report))
        all_rooms = RoomInfo.objects.filter(room__accommodation=accommodation)
        reserved = all_rooms.filter(Q(reservation__check_in__gte=date.today()) |
                                    Q(reservation__check_out__lte=date.today()), reservation__is_canceled=False)
        out_of_service = all_rooms.filter(Q(roomoutofservice__from_date__gte=date.today()) |
                                          Q(roomoutofservice__to_date__lte=date.today()))
        empty_rooms = all_rooms.difference(reserved)
        empty_rooms = empty_rooms.difference(out_of_service)
        context['report'] = report
        context['empty_rooms'] = empty_rooms
        context['reserved'] = reserved
        context['out_of_service'] = out_of_service
        return context

    def convert_string_to_date(self, date_string):
        split_string = [int(x.translate(trans_num)) for x in date_string.split('/')]
        return JalaliDate(split_string[0], split_string[1], split_string[2]).todate()
