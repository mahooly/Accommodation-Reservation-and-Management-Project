from django.shortcuts import render
from django.views.generic import ListView

from .filters import AccommodationFilter
from accommodation.models import Accommodation
from django.views import View
from .forms import LocationSearchForm
from django.db.models import Q



# Create your views here.

# def search_list(request):
#     f = AccommodationFilter(request.GET, queryset=Accommodation.objects.all())
#     return render(request, 'search_index/search.html', {'filter': f})
class MainPageView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Accommodation.objects.filter(is_authenticated=True)


class SearchView(View):
    template_name = 'search_index/search.html'

    def get(self, request, *args, **kwargs):
        f = AccommodationFilter(request.GET, queryset=Accommodation.objects.all())
        return render(request, self.template_name, {'filter': f})

class LocationSearchView(View):

    def get(self, request, *args, **kwargs):
        form = LocationSearchForm(request.GET)
        if form.is_valid():
            exp = form.cleaned_data['expression']
            qs = Accommodation.objects.filter(Q(title__icontains=exp) | 
                                Q(description__icontains=exp) | Q(city__icontains=exp) | Q(province__icontains=exp))
            print('%' * 10)
            print(qs)
            print(exp)
            return render(request, 'search_index/search_results.html', {'results': qs})
            