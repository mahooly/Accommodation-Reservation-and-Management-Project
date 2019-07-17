from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Host


class CustomUserCreationForm(UserCreationForm):
    birthday = forms.CharField(max_length=10)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'birthday', 'gender', 'image')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'gender', 'image')

    def clean_password(self):
        return ''


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ('city', 'passport_pic', 'home_address', 'phone_number')
