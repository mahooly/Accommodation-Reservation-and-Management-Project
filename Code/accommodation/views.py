from django.shortcuts import render, redirect
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