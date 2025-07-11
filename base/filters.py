import django_filters
from .models import UserProfile, GroupProfile, Menu, Department


class UserProfileFilter(django_filters.FilterSet):
    user__username = django_filters.CharFilter(
        lookup_expr='icontains',
        label='User Name contains'
        )
    
    user__first_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='First Name contains'
        )
    
    user__last_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Last Name contains'
        )

    class Meta:
        fields = ['user__username','user__first_name' ,'user__last_name']
        model = UserProfile

class GroupProfileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        fields = ['name']
        model = GroupProfile

class MenuFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    module = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        fields = ['name', 'module']
        model = Menu


class DepartmentFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        fields = ['code', 'name']
        model = Department