from django import forms


class LocationSearchForm(forms.Form):
    expression = forms.CharField(label='expression', max_length=20)


class FilterForm(forms.Form):
    province = forms.CharField(max_length=40, required=False)
    hotel = forms.BooleanField(required=False)
    motel = forms.BooleanField(required=False)
    house = forms.BooleanField(required=False)
    city = forms.CharField(max_length=40, required=False)
    

