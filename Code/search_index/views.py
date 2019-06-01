from django.shortcuts import render
from django.views.generic import ListView

from .filters import AccommodationFilter
from accommodation.models import Accommodation
from django.views import View


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
