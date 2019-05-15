from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from Makan_System.forms import CustomUserCreationForm


def index(request):
    # TODO: index.html
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        signupform = CustomUserCreationForm(data=request.POST)

        if signupform.is_valid():
            username = signupform.cleaned_data['username']
            password = signupform.cleaned_data['password1']
            signupform.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        signupform = CustomUserCreationForm()
    return render(request, 'register.html', {'form': signupform})
