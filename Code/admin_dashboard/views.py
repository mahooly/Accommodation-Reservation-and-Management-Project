from django.shortcuts import render, get_object_or_404, redirect
from registration.models import CustomUser
from accommodation.models import Accommodation
from django.views import View

# Create your views here.

class AdminDashboard(View):
    template_name = 'admin_dashboard.html'

    all_users = CustomUser.objects.all()
    all_accommodations = Accommodation.objects.all()

    def get(self, request, *args, **kwargs):
        context = {'users': self.all_users, 'accommodations':self.all_accommodations}
        return render(request, self.template_name, context=context)

class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_pk = kwargs['pk']
        user = get_object_or_404(CustomUser, pk=user_pk)
        user.delete()
        return redirect('/admin_dashboard')

class DeleteAccommodation(View):
    def get(self, request, *args, **kwargs):
        acc_pk = kwargs['pk']
        acc = get_object_or_404(Accommodation, pk=acc_pk)
        acc.delete()
        return redirect('/admin_dashboard')

class AuthenticateAccommodation(View):
    def get(self, request, *args, **kwargs):
        acc_pk = kwargs['pk']
        acc = get_object_or_404(Accommodation, pk=acc_pk)
        acc.is_authenticated = True
        acc.save()
        return redirect('/admin_dashboard')