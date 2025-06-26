import django_filters
from .models import DocHeader


class DocHeaderFilter(django_filters.FilterSet):
    class Meta:
        fields = {'groups': ['exact'], }
        model = DocHeader
