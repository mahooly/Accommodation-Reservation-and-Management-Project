from django import forms
from .models import Accommodation, Amenity, Room, Image


class AccommodationCreationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['accommodation_type', 'title', 'description', 'province', 'city', 'address', 'email',
                  'phone']


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['how_many', 'bed_type', 'number_of_guests']


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = '__all__'


class AccommodationChangeForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['accommodation_type', 'title', 'description', 'address', 'email',
                  'phone']


class FileFieldForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
