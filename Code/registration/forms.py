from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Host


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'gender', 'image')


class HostForm(forms.ModelForm):
    class Meta():
        model = Host
        fields = ('passport_pic','home_address','phone_number')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'gender','password')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.PasswordInput()

