from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from .forms import AccommodationCreationForm, AmenityForm, RoomCreationForm
from .models import Accommodation, Room


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


# class AccommodationDetailView(DetailView):
#     model = Accommodation
#     template_name = 'accommodation_detail.html'

class AccommodationDetailView(View):
    # model = Accommodation
    template_name = 'accommodation_detail.html'

    def get(self, request, *args, **kwargs):
        acc_id = kwargs['pk']
        acc = get_object_or_404(Accommodation, pk=acc_id)
        guest_num, room_num, twin_num, single_num, double_num = 0, 0, 0, 0, 0
        rooms = Room.objects.filter(accommodation=acc)
        for r in rooms:
            room_num += r.how_many
            guest_num += (r.how_many * r.number_of_guests)
            if r.bed_type == 'Single':
                single_num += r.how_many
            elif r.bed_type == 'Double':
                double_num += r.how_many
            elif r.bed_type == 'Twin':
                twin_num += r.how_many
        acc_d = {}
        acc_d['room_num'] = room_num
        acc_d['single_num'] = single_num
        acc_d['double_num'] = double_num
        acc_d['twin_num'] = twin_num
        acc_d['guest_num'] = guest_num

        context = {'accommodation': acc, 'accommodation_details': acc_d}
        return render(request, self.template_name, context=context)

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
            room.save()
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)
        else:
            print('%' * 100)
