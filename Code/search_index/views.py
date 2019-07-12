import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView
from khayyam import JalaliDate

from .filters import AccommodationFilter
from accommodation.models import Accommodation, RoomInfo, Room
from django.views import View
from .forms import LocationSearchForm, FilterForm
from django.db.models import Q

persian_numbers = '۱۲۳۴۵۶۷۸۹۰'
english_numbers = '1234567890'
trans_num = str.maketrans(persian_numbers, english_numbers)


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
        check_in = request.GET.get('check_in', '')
        check_out = request.GET.get('check_out', '')
        price = request.GET.get('price', '')
        price_low = 200
        price_high = 500

        if is_hotel or is_motel or is_house:
            q = self.filter_by_type(q, is_hotel, is_motel, is_house)

        if check_in:
            q = self.filter_by_date(q, check_in, check_out)

        if price:
            q = self.filter_by_price(q, price)
            price_low = price.split('-')[0]
            price_high = price.split('-')[1]

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
            'check_in': check_in,
            'check_out': check_out,
            'price': price,
            'url': self.build_url(expression, province, city, is_hotel, is_motel, is_house, check_in, check_out, price),
            'is_hotel': is_hotel,
            'is_motel': is_motel,
            'is_house': is_house,
            'price_low': price_low,
            'price_high': price_high
        }
        return render(request, self.template_name, context)

    def filter_by_type(self, q, is_hotel, is_motel, is_house):
        q = q.filter(
            Q(accommodation_type__iexact=is_hotel) | Q(accommodation_type__iexact=is_motel) | Q(
                accommodation_type__iexact=is_house))
        return q

    def filter_by_date(self, q, check_in, check_out):
        check_in = self.convert_string_to_date(check_in)
        check_out = self.convert_string_to_date(check_out)

        availableRoomInfos1 = RoomInfo.objects.all().exclude(
            Q(reservation__check_in__range=(check_in, check_out - datetime.timedelta(days=1))),
            Q(reservation__is_canceled=False))
        availableRoomInfos2 = availableRoomInfos1.exclude(
            Q(reservation__check_out__range=(check_in + datetime.timedelta(days=1), check_out)),
            Q(reservation__is_canceled=False))
        availableRoomInfos = availableRoomInfos2.filter(out_of_service=False)
        rooms = Room.objects.filter(roominfo__in=availableRoomInfos).distinct()
        q = q.filter(room__in=rooms).distinct()
        return q

    def filter_by_price(self, q, price):
        price_low = int(price.split('-')[0]) * 1000
        price_high = int(price.split('-')[1]) * 1000
        if price_high == 900 * 1000:
            rooms = Room.objects.filter(price__gte=price_low)
        else:
            rooms = Room.objects.filter(price__gte=price_low, price__lte=price_high)
        q = q.filter(room__in=rooms).distinct()
        return q

    def build_url(self, expression, province, city, is_hotel, is_motel, is_house, check_in, check_out, price):
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
        if check_in:
            url += '?check_in=' + check_in if first else '&check_in=' + check_in
            first = False
        if check_out:
            url += '?check_out=' + check_out if first else '&check_out=' + check_out
            first = False
        if price:
            url += '?price=' + price if first else '&price=' + price
            first = False
        return url

    def convert_string_to_date(self, date_string):
        split_string = [int(x.translate(trans_num)) for x in date_string.split('/')]
        return JalaliDate(split_string[0], split_string[1], split_string[2]).todate()
