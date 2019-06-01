from django import forms


class LocationSearchForm(forms.Form):
    expression = forms.CharField(label='expression', max_length=20)
    

