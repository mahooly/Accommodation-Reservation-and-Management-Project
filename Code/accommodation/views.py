from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView

from Code.settings import DEFAULT_FROM_EMAIL
from .forms import AccommodationCreationForm, AmenityForm, RoomCreationForm, AccommodationChangeForm, FileFieldForm, RoomSearchForm
from .models import Accommodation, Amenity, Image, RoomInfo, Room
from registration.decorators import user_is_host
from .decorators import user_same_as_accommodation_user, user_host_or_superuser, user_same_as_image_user
from datetime import timedelta
import time
from reservation.models import Reservation
from registration.models import CustomUser
from django.db.models import Q
import datetime
import math

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


class AccommodationDetailView(View):
    #model = Accommodation
    format = '%m/%d/%Y'
    template_name = 'accommodation/accommodation_detail.html'


    def get(self, request, pk):
        accommodation = get_object_or_404(Accommodation, pk=pk)
        rooms = Room.objects.filter(accommodation__id__exact=pk)
        form = RoomCreationForm()
        print("rooms shit is ", rooms)
        print("full path is ", request.get_full_path)
        context = {'accommodation': accommodation, 'form': form, 'room_amenities':Amenity.objects.filter(label='room'), 'rooms':rooms,
                   'hotel_amenities':Amenity.objects.filter(label='hotel')}
        #print("date2 is ", self.convert_date_to_string(datetime.datetime.now()))
        #print("date is ", self.convert_string_to_date(self.convert_date_to_string(datetime.datetime.now())))

        #if 'check_in' not in request.GET:
        #    return render(request, self.template_name, context)

        form = RoomSearchForm(request.GET)
        if not form.is_valid():
            print("search form is not valid, please try again")
            return render(request, self.template_name, context)

        print("rooms1 shit is ",rooms)
        ## filtering based on check_in & check_out
        #check_in = datetime.date(2019, 7, 8)
        #check_out = datetime.date(2019, 7, 10)
        if form.cleaned_data['check_in']:
            check_in = form.cleaned_data['check_in']
            check_out = check_in + timedelta(days=form.cleaned_data['check_out'])
            availableRoomInfos = RoomInfo.objects.all().exclude(
                Q(reservation__check_in__range=(check_in, check_out - timedelta(days=1))) |
                Q(reservation__check_out__range=(check_in + timedelta(days=1), check_out))).filter(out_of_service=False)
            print("rooms2.5 shit is ", availableRoomInfos)
            rooms = rooms.filter(roominfo__in=availableRoomInfos).distinct()

            ## updating context
            context['check_in'] = self.convert_date_to_string_2(check_in)
            context['check_out'] = form.cleaned_data['check_out']

        print("rooms2 shit is ", rooms)

        money_low = 300000
        money_high = 0
        flag = False
        infinit = 100000000
        if form.cleaned_data['money_first']:
            flag = True
            money_low = min(money_low, 0)
            money_high = max(money_high, 100000)
        if form.cleaned_data['money_second']:
            flag = True
            money_low = min(money_low, 100000)
            money_high = max(money_high, 200000)
        if form.cleaned_data['money_third']:
            flag = True
            money_low = min(money_low, 200000)
            money_high = max(money_high, 300000)
        if form.cleaned_data['money_forth']:
            flag = True
            money_low = min(money_low, 300000)
            money_high = max(money_high, infinit)
        if flag:
            rooms = rooms.filter(price__gte=money_low).filter(price__lte=money_high)

        print("rooms3 shit is ",rooms)


        for amenity in Amenity.objects.all():
            if amenity.name in request.GET:
                print("Filtering for an amenity!")
                rooms = rooms.filter(amenity__name=amenity.name)


        print("rooms are ",rooms)


        #reservations = Reservation(reserver=CustomUser.objects.all()[0], room=RoomInfo., check_in=datetime.date(2019, 1, 1), check_out=5)
       # rooms = rooms.filter()

        context['rooms'] = rooms
        return render(request, self.template_name, context)

    #def post(self, request, pk):
    #    print(" here")
    #    form = RoomSearchForm(request.POST)
    #    print("money first is  ", form.money_first)
    #    accommodation = get_object_or_404(Accommodation, pk=pk)
    #    form = RoomCreationForm()
    #    context = {'accommodation': accommodation, 'form': form}
    #    return render(request, self.template_name, context)

    def build_url(self, check_out, check_in, money_low, money_high, is_hotel, is_motel, is_house):
        url = ''
        first = True
        if night_number:
            url += '?check-in='
            first = False
        if arrival_date:
            url += ('?arrival_date=' if first else '&arrival_date') + self.convert_date_to_string(check_in)
            first = False
        if money_low:
            url += ('?money_low=' if first else '&city')  + str(money_low)
            first = False
        if money_high:
            url += ('?money_high=' if first else '&city')  + str(money_high)
            first = False
        if is_hotel:
            url += '?hotel=on' if first else '&hotel=on'
            first = False
        if is_motel:
            url += '?motel=on' if first else '&motel=on'
            first = False
        if is_house:
            url += '?house=on' if first else '&house=on'
            first = False
        return url

    def convert_string_to_date(self, date_string):
        return datetime.datetime.strptime(date_string, self.format)

    def convert_date_to_string(self, datetime_object):
        return datetime_object.strftime(self.format)

    def convert_date_to_string_2(self, datetime_object):
        format2 = '%Y-%m-%d'
        return datetime_object.strftime(format2)
        #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    form = RoomCreationForm()
    #    context['form'] = form
    #    return context


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

