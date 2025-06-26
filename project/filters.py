import django_filters
from .models import Site, BudgetItem, Activity, Task, Category, Work, UserWorkDate, DailyWork


class SiteFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name']
        model = Site


class BudgetItemFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name', 'site', 'type', 'amount']
        model = BudgetItem


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name']
        model = Category


class ActivityFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name', 'site', 'start_date', 'leader']
        model = Activity


class TaskFilter(django_filters.FilterSet):
    class Meta:
        fields = ['activity','sequence','code','name', 'leader']
        model = Task


class WorkFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code']
        model = Work


class UserWorkDateFilter(django_filters.FilterSet):
    class Meta:
        fields = ['user']
        model = UserWorkDate


class DailyWorkFilter(django_filters.FilterSet):
    class Meta:
        fields = ['work']
        model = DailyWork
