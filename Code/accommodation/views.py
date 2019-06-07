from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView

from Code.settings import DEFAULT_FROM_EMAIL
from .forms import AccommodationCreationForm, AmenityForm, RoomCreationForm, AccommodationChangeForm, FileFieldForm
from .models import Accommodation, Room, Amenity, Image
from django.views.generic import ListView


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
    template_name = 'accommodation/accommodation_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RoomCreationForm()
        context['form'] = form
        return context


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
            messages.success(request, 'اتاق با موفقیت اضافه شد.')
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)
        else:
            print(form.errors)
            messages.error(request, 'در اضافه کردن اتاق مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)


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


class EditAccommodation(View):
    template_name = 'accommodation/edit_accommodation.html'

    def get(self, request, *args, **kwargs):
        accommodation_id = kwargs['pk']
        images = Image.objects.filter(accommodation_id=accommodation_id)
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        amenity = accommodation.amenity
        form = AccommodationChangeForm(instance=accommodation,
                                       initial={'title': accommodation.title,
                                                'accommodation_type': accommodation.accommodation_type,
                                                'description': accommodation.description,
                                                'address': accommodation.address, 'email': accommodation.email,
                                                'phone': accommodation.phone,
                                                'city': accommodation.city,
                                                'province': accommodation.province,
                                                'images': images})
        amenity_form = AmenityForm(instance=amenity,
                                   initial={'has_tv': amenity.has_tv, 'has_wifi': amenity.has_wifi,
                                            'has_warm_ac': amenity.has_warm_ac,
                                            'has_cool_ac': amenity.has_cool_ac, 'has_elevator': amenity.has_elevator,
                                            'has_parking': amenity.has_parking, 'has_kitchen': amenity.has_kitchen,
                                            'has_utensils': amenity.has_utensils, 'has_oven': amenity.has_oven,
                                            'has_fridge': amenity.has_fridge,
                                            'has_roomservice': amenity.has_roomservice,
                                            'has_safe': amenity.has_safe, 'has_iron': amenity.has_iron
                                            })
        image_form = FileFieldForm()
        return render(request, self.template_name,
                      {'form': form, 'amenity_form': amenity_form, 'image_form': image_form})

    def post(self, request, *args, **kwargs):
        accommodation_id = kwargs['pk']
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        amenity = accommodation.amenity
        images = Image.objects.filter(accommodation_id=accommodation_id)
        form = AccommodationChangeForm(request.POST, request.FILES, instance=accommodation)
        amenity_form = AmenityForm(request.POST, instance=amenity)
        image_form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid() and amenity_form.is_valid() and image_form.is_valid():
            form.save()
            amenity_form.save()
            messages.success(request, 'اطلاعات شما با موفقیت ثبت شد.')
            files = request.FILES.getlist('image')
            for f in files:
                Image.objects.create(accommodation=accommodation, image=f)
        form = AccommodationChangeForm(instance=accommodation,
                                       initial={'title': accommodation.title,
                                                'accommodation_type': accommodation.accommodation_type,
                                                'description': accommodation.description,
                                                'address': accommodation.address, 'email': accommodation.email,
                                                'phone': accommodation.phone,
                                                'city': accommodation.city,
                                                'province': accommodation.province,
                                                'images': images})
        amenity_form = AmenityForm(instance=amenity,
                                   initial={'has_tv': amenity.has_tv, 'has_wifi': amenity.has_wifi,
                                            'has_warm_ac': amenity.has_warm_ac,
                                            'has_cool_ac': amenity.has_cool_ac, 'has_elevator': amenity.has_elevator,
                                            'has_parking': amenity.has_parking, 'has_kitchen': amenity.has_kitchen,
                                            'has_utensils': amenity.has_utensils, 'has_oven': amenity.has_oven,
                                            'has_fridge': amenity.has_fridge,
                                            'has_roomservice': amenity.has_roomservice,
                                            'has_safe': amenity.has_safe, 'has_iron': amenity.has_iron
                                            })
        image_form = FileFieldForm()
        return render(request, self.template_name,
                      {'form': form, 'amenity_form': amenity_form, 'image_form': image_form})


class DeleteImage(View):
    def get(self, request, *args, **kwargs):
        img_pk = kwargs['pk']
        img = get_object_or_404(Image, pk=img_pk)
        accommodation = img.accommodation
        img.delete()
        url = '/edit_accommodation/' + str(accommodation.pk)
        messages.success(request, 'عکس با موفقیت حذف شد.')
        return redirect(url)


class CreateAmenityView(View):
    def post(self, request, *args, **kwargs):
        form = AmenityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'امکانات با موفقیت اضافه شد.')
        else:
            messages.error(request, 'در اضافه کردن امکانات مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')
        return redirect('/create_accommodation/')
