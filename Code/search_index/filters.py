import django_filters
from accommodation.models import Accommodation

class AccommodationFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    accommodation_type = django_filters.CharFilter(field_name='accommodation_type', lookup_expr='iexact')
    province = django_filters.CharFilter(field_name='province', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')

    class Meta:
        model = Accommodation
        fields = ['title', 'accommodation_type', 'province', 'city']