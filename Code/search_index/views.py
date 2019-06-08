from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView

from .filters import AccommodationFilter
from accommodation.models import Accommodation
from django.views import View
from .forms import LocationSearchForm, FilterForm
from django.db.models import Q


class MainPageView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Accommodation.objects.filter(is_authenticated=True)


class SearchView(View):
    template_name = 'search_index/search.html'

    def get(self, request, *args, **kwargs):
        form = LocationSearchForm(request.GET)
        q = Accommodation.objects.filter(is_authenticated=True)
        if form.is_valid():
            exp = form.cleaned_data['expression']
            q = q.filter(Q(title__icontains=exp) |
                         Q(description__icontains=exp) | Q(city__icontains=exp) | Q(
                province__icontains=exp))

        is_hotel = 'هتل' if request.GET.get('hotel', '') else ''
        is_motel = 'اقامتگاه' if request.GET.get('motel', '') else ''
        is_house = 'منزل شخصی' if request.GET.get('house', '') else ''

        if is_hotel or is_motel or is_house:
            q = q.filter(
                Q(accommodation_type__iexact=is_hotel) | Q(accommodation_type__iexact=is_motel) | Q(
                    accommodation_type__iexact=is_house))
        q = AccommodationFilter(request.GET, queryset=q).qs

        paginator = Paginator(q, 5)
        page = request.GET.get('page')
        content = paginator.get_page(page)

        province = request.GET.get('province', '')
        city = request.GET.get('city', '')
        expression = request.GET.get('expression', '')

        context = {
            'content': content,
            'form': form,
            'expression': expression,
            'province': province,
            'city': city,
            'url': self.build_url(expression, province, city, is_hotel, is_motel, is_house),
            'is_hotel': is_hotel,
            'is_motel': is_motel,
            'is_house': is_house
        }
        return render(request, self.template_name, context)

    def build_url(self, expression, province, city, is_hotel, is_motel, is_house):
        url = ''
        first = True
        if expression:
            url += '?expression=' + expression
            first = False
        if province:
            url += '?province=' + province if first else '&province' + province
            first = False
        if city:
            url += '?city=' + city if first else '&city' + city
            first = False
        if is_hotel:
            url += '?hotel=on' if first else '&hotel=on'
            first = False
        if is_motel:
            url += '?motel=on' if first else '&motel=on'
            first = False
        if is_house:
            url += '?house=on' if first else '&house=on'
            first = False
        return url
