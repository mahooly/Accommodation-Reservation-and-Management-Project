from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView

from .filters import AccommodationFilter
from accommodation.models import Accommodation
from django.views import View
from .forms import LocationSearchForm
from django.db.models import Q


class MainPageView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Accommodation.objects.filter(is_authenticated=True)


class SearchView(View):
    template_name = 'search_index/search.html'

    def get(self, request, *args, **kwargs):
        f = AccommodationFilter(request.GET, queryset=Accommodation.objects.all())
        paginator = Paginator(f.qs, 10)
        page = request.GET.get('page')
        filtered = paginator.get_page(page)
        if len(args) > 0:
            dummy = args[0]
            init = args[1]
        else:
            dummy = []
            init = False
        return render(request, self.template_name, {'filter': filtered, 'results': dummy, 'init': init})


class LocationSearchView(View):
    def get(self, request, *args, **kwargs):
        form = LocationSearchForm(request.GET)
        if form.is_valid():
            exp = form.cleaned_data['expression']
            qs = Accommodation.objects.filter(Q(title__icontains=exp) |
                                              Q(description__icontains=exp) | Q(city__icontains=exp) | Q(
                province__icontains=exp))
            print('%' * 10)
            print(qs)
            print(exp)

            sv = SearchView()
            response = sv.get(request, qs, True)
            return response
            # return render(request, 'search_index/search.html', {'results': qs, 'filter': f, 'init': True})
