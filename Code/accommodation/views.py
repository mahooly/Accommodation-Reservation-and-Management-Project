from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from .forms import AccommodationCreationForm, AmenityForm, RoomCreationForm
from .models import Accommodation

# Create your views here.

class CreateAccommodationView(View):
    template_name = 'create_accommodation.html'

    def get(self, request, *args, **kwargs):
        form = AccommodationCreationForm()
        amenity_form = AmenityForm()
        return render(request, self.template_name, {'form': form, 'amenity_form': amenity_form})
    
    def post(self, request, *args, **kwargs):
        form = AccommodationCreationForm(request.POST, request.FILES)
        amenity_form = AmenityForm(request.POST)
        if form.is_valid() and amenity_form.is_valid():
            owner = request.user.host
            house = form.save(commit=False)
            house.owner = owner
            amenity = amenity_form.save()
            house.amenity = amenity
            house.save()
            url = '/accommodation/' + str(house.pk)
            return redirect(url)
            # TODO go to detail view of house
        else:
            print('%' * 100)


class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'accommodation_detail.html'


class CreateRoomView(View):
    template_name = 'create_room.html'

    def get(self, request, *args, **kwargs):
        form = RoomCreationForm()
        amenity_form = AmenityForm()
        return render(request, self.template_name, {'form': form, 'amenity_form': amenity_form})
    
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
            house.save()
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)
            # TODO go to detail view of house
        else:
            print('%' * 100)