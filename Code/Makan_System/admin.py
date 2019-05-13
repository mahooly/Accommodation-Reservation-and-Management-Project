from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Makan_System.forms import CustomUserCreationForm, CustomUserChangeForm
from Makan_System.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'image']

admin.site.register(CustomUser, CustomUserAdmin)
