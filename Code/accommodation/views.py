from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView

from Code.settings import DEFAULT_FROM_EMAIL
from .forms import AccommodationCreationForm, AmenityForm, RoomCreationForm, AccommodationChangeForm, FileFieldForm
from .models import Accommodation, Amenity, Image
from registration.decorators import user_is_host
from .decorators import user_same_as_accommodation_user, user_host_or_superuser, user_same_as_image_user


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
    template_name = 'accommodation/accommodation_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RoomCreationForm()
        context['form'] = form
        return context


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
            messages.success(request, 'اتاق با موفقیت اضافه شد.')
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)
        else:
            print(form.errors)
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
