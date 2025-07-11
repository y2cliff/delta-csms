import django_filters
from .models import InvCategory


class InvCategoryFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name']
        model = InvCategory