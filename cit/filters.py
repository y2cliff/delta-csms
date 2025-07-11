import django_filters
from .models import Manufacturer, Radio, RadioLicense


class ManufacturerFilter(django_filters.FilterSet):
    class Meta:
        fields = ['code','name']
        model = Manufacturer


class RadioFilter(django_filters.FilterSet):
    class Meta:
        fields = ['site','manufacturer', 'model', 'type']
        model = Radio


class RadioLicenseFilter(django_filters.FilterSet):
    class Meta:
        fields = ['license_number','radio']
        model = RadioLicense
