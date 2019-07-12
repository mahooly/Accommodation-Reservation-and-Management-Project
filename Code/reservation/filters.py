import django_filters

from reservation.models import Reservation


class ReservationFilter(django_filters.FilterSet):
    check_in_range = django_filters.DateRangeFilter(name='check_in')
    check_out_range = django_filters.DateRangeFilter(name='check_out')

    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out']
