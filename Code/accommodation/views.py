from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from .forms import AccommodationCreationForm, AmenityForm, RoomCreationForm, AccommodationChangeForm, ImageForm, \
    FileFieldForm
from .models import Accommodation, Room, Amenity, Image
from django.views.generic import ListView


class CreateAccommodationView(View):
    template_name = 'accommodation/create_accommodation.html'

    def get(self, request, *args, **kwargs):
        form = AccommodationCreationForm()
        amenity_form = AmenityForm()
        image_form = FileFieldForm()
        return render(request, self.template_name,
                      {'form': form, 'amenity_form': amenity_form, 'image_form': image_form})

    def post(self, request, *args, **kwargs):
        form = AccommodationCreationForm(request.POST, request.FILES)
        amenity_form = AmenityForm(request.POST)
        image_form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid() and amenity_form.is_valid() and image_form.is_valid():
            owner = request.user.host
            house = form.save(commit=False)
            house.owner = owner
            amenity = amenity_form.save()
            house.amenity = amenity
            house.save()
            files = request.FILES.getlist('image')
            for f in files:
                Image.objects.create(accommodation=house, image=f)
            url = '/accommodation/' + str(house.pk)
            return redirect(url)
        else:
            return render(request, self.template_name,
                          {'form': form, 'amenity_form': amenity_form, 'image_form': image_form})


class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'accommodation/accommodation_detail.html'


class CreateRoomView(View):
    def post(self, request, *args, **kwargs):
        form = RoomCreationForm(request.POST)
        amenity_form = AmenityForm(request.POST)
        if form.is_valid() and amenity_form.is_valid():
            accommodation_id = kwargs['accid']
            accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
            room = form.save(commit=False)
            room.accommodation = accommodation
            amenity = amenity_form.save()
            room.amenity = amenity
            room.save()
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)
        else:
            print('%' * 100)


class DeleteAccommodation(View):
    def get(self, request, *args, **kwargs):
        acc_pk = kwargs['pk']
        acc = get_object_or_404(Accommodation, pk=acc_pk)
        acc.delete()
        if request.user.is_host:
            return redirect('/host_dashboard')
        else:
            return redirect('/admin_dashboard/accommodations')


class EditAccommodation(View):
    template_name = 'accommodation/edit_accommodation.html'

    def get(self, request, *args, **kwargs):
        accommodation_id = kwargs['pk']
        images = Image.objects.filter(accommodation_id=self.kwargs['pk'])
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
        form = AccommodationChangeForm(request.POST, request.FILES, instance=accommodation)
        amenity_form = AmenityForm(request.POST, instance=amenity)
        image_form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid() and amenity_form.is_valid() and image_form.is_valid():
            form.save()
            amenity_form.save()
            files = request.FILES.getlist('image')
            for f in files:
                Image.objects.create(accommodation=accommodation, image=f)
            url = '/edit_accommodation/' + str(accommodation.pk)
            return redirect(url)
        return render(request, self.template_name, {'form': form, 'amenity_form': amenity_form})


class AccommodationRoomsView(ListView):
    template_name = 'accommodation/room_list.html'

    def get_queryset(self):
        acc = get_object_or_404(Accommodation, pk=self.kwargs['pk'])
        return Room.objects.filter(accommodation=acc)


class DeleteImage(View):
    def get(self, request, *args, **kwargs):
        img_pk = kwargs['pk']
        img = get_object_or_404(Image, pk=img_pk)
        accommodation = img.accommodation
        img.delete()
        url = '/edit_accommodation/' + str(accommodation.pk)
        return redirect(url)
