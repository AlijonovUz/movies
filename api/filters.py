import django_filters
from .models import Movies


class MovieFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')

    class Meta:
        model = Movies
        fields = ['genre']
