import django_filters
from .models import UserProfile, Menu


class UserProfileFilter(django_filters.FilterSet):
    company = django_filters.TypedChoiceFilter(
        field_name='company',
        label='Organization',
        # null_label='Uncategorized',
        # queryset=Module.objects.filter(nameentity_type='PR'),
    )

    class Meta:
        fields = ['company']
        model = UserProfile


class MenuFilter(django_filters.FilterSet):
    class Meta:
        fields = ['name', 'module']
        model = Menu