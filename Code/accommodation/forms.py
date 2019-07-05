from django import forms

from .models import Accommodation, Amenity, Room


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
    how_many = forms.IntegerField()

    class Meta:
        model = Room
        fields = ['bed_type', 'number_of_guests', 'amenity', 'description', 'image']

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

class RoomSearchForm(forms.Form):
    check_in = forms.DateField(required=False)
    check_out = forms.IntegerField(required=False)
    money_first = forms.BooleanField(required=False)
    money_second = forms.BooleanField(required=False)
    money_third = forms.BooleanField(required=False)
    money_forth = forms.BooleanField(required=False)
    is_hotel = forms.BooleanField(required=False)
    is_motel = forms.BooleanField(required=False)
    is_house = forms.BooleanField(required=False)