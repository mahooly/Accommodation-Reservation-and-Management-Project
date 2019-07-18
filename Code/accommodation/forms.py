from django import forms
from django.forms import CheckboxInput

from .models import Accommodation, Amenity, Room, RoomInfo


class AccommodationCreationForm(forms.ModelForm):
    lat = forms.CharField(max_length=20)
    long = forms.CharField(max_length=20)

    class Meta:
        model = Accommodation
        fields = ['accommodation_type', 'title', 'description', 'province', 'city', 'address', 'email',
                  'phone', 'amenity', 'lat', 'long']

    def __init__(self, *args, **kwargs):
        super(AccommodationCreationForm, self).__init__(*args, **kwargs)
        self.fields["amenity"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["amenity"].queryset = Amenity.objects.all()


class RoomCreationForm(forms.ModelForm):
    how_many = forms.IntegerField()

    class Meta:
        model = Room
        fields = ['bed_type', 'number_of_guests', 'amenity', 'description', 'image', 'price']

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
                  'phone', 'amenity', 'latitude', 'longitude', 'is_inactive']
        widgets = {
            'is_inactive': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
        }
        labels = {'is_inactive': 'اقامتگاه غیرفعال است'}

    def __init__(self, *args, **kwargs):
        super(AccommodationChangeForm, self).__init__(*args, **kwargs)
        self.fields["amenity"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["amenity"].queryset = Amenity.objects.all()


class FileFieldForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class RoomInfoForm(forms.ModelForm):
    class Meta:
        model = RoomInfo
        exclude = ('room',)
