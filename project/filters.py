import django_filters
from .models import Site, BudgetItem, Activity, Task, ProjCategory, Work, UserWorkDate, DailyWork
from .forms import UserSelect2Widget
from django_select2.forms import Select2Widget
from django.contrib.auth.models import User
from base.forms import Helper, SELECTFILTER_CSS, ClearableSelect2Widget

class SiteFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name']
        model = Site


class BudgetItemFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name', 'site', 'type', 'amount']
        model = BudgetItem


class ProjCategoryFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name']
        model = ProjCategory


class ActivityFilter(django_filters.FilterSet):
    leader = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=Select2Widget,
        label='Leader'
    )
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
    user =django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=ClearableSelect2Widget(attrs={"data-placeholder": "select an option"}),
        label='Filter by User'
        )

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    class Meta:
        fields = ['user']
        model = UserWorkDate


class DailyWorkFilter(django_filters.FilterSet):
    class Meta:
        fields = ['work']
        model = DailyWork
