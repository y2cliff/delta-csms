import django_tables2 as tables
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Manufacturer, Radio, RadioLicense
from base.tables import ATTRS
from django import forms


class ManufacturerTable(tables.Table):
    code = tables.Column(linkify=True)

    class Meta:
        model = Manufacturer
        attrs = ATTRS
        fields = sequence = ('code', 'name', 'is_active', 'date_created', 'date_updated')

    def render_is_active(self, value):
        if value:
            return 'Active'
        return 'Inactive'


class RadioTable(tables.Table):
    serial_number = tables.Column(linkify=True)
    site = tables.Column(accessor='site.code', verbose_name="Site")
     
    class Meta:
        model = Radio
        attrs = ATTRS
        fields = sequence = ('serial_number', 'manufacturer', 'model', 'site', 'type', 'frequency_band', 'status')

    # def render_amount(self, value):
    #     return intcomma(value)


class RadioLicenseTable(tables.Table):
    license_number = tables.Column(linkify=True)
    
    class Meta:
        model = RadioLicense
        attrs = ATTRS
        fields = sequence = ('license_number', 'radio', 'effective_date', 'expiry_date')


