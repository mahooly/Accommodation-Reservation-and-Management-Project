from django import forms

from .models import Accommodation, Amenity, Room, Image


class AccommodationCreationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['accommodation_type', 'title', 'description', 'province', 'city', 'address', 'email',
                  'phone', 'amenity']

    def __init__(self, *args, **kwargs):
        super(AccommodationCreationForm, self).__init__(*args, **kwargs)
        self.fields["amenity"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["amenity"].queryset = Amenity.objects.all()


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['how_many', 'bed_type', 'number_of_guests', 'amenity', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(RoomCreationForm, self).__init__(*args, **kwargs)
        self.fields["amenity"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["amenity"].queryset = Amenity.objects.filter(label='room')


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = '__all__'


class AccommodationChangeForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['accommodation_type', 'title', 'description', 'address', 'email',
                  'phone', 'amenity']

    def __init__(self, *args, **kwargs):
        super(AccommodationChangeForm, self).__init__(*args, **kwargs)
        self.fields["amenity"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["amenity"].queryset = Amenity.objects.all()


class FileFieldForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
