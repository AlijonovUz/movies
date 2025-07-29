import django_filters
from .models import Movie


class MovieFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')
    year = django_filters.NumberFilter(field_name='year', lookup_expr='iexact')
    country = django_filters.CharFilter(field_name='country__slug', lookup_expr='iexact')

    class Meta:
        model = Movie
        fields = ['genre', 'year', 'country']
