from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

from django_select2.forms import Select2Widget

from crispy_forms.layout import Field, Row, Column, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

from base.forms import Helper, SELECTFILTER_CSS, ClearableSelect2Widget
from .models import Manufacturer, Radio, RadioLicense
from django_currentuser.middleware import get_current_user
import datetime


from django.utils.safestring import mark_safe


class ManufacturerForm(forms.ModelForm):

    class Meta:
        model = Manufacturer
        fields = ['code','name']

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
            Column(FloatingField('code'),css_class="col-lg-2"),   
            Column(FloatingField('name'),css_class="col-lg-10")
            )
        )
        super(ManufacturerForm, self).__init__(*args, **kwargs)


    # def clean_code(self):
    #     code = self.cleaned_data['code']
    #     if not self.instance and Site.objects.filter(code=code).exists():
    #         raise forms.ValidationError(f"Code already exists.")
    #     return code

    def get_cancel_url(self):
        return reverse('cit:manufacturer-list')


class RadioForm(forms.ModelForm):

    class Meta:
        model = Radio
        fields = ['serial_number','manufacturer', 'site', 'model','type', 'frequency_band','frequency','status']
        widgets = {
            'site': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
            # 'type': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
        }

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('type'),css_class="col-lg-4"),
                Column(FloatingField('manufacturer'),css_class="col-lg-4"),
                Column(FloatingField('model'),css_class="col-lg-4")
            ),
            Row(
                Column(FloatingField('frequency_band'),css_class="col-lg-4"),
                Column(FloatingField('frequency'),css_class="col-lg-4"),
                Column(FloatingField('serial_number'),css_class="col-lg-4")
            ),
            Row(
                Column(FloatingField('site'),css_class="col-lg-6"),
                Column(FloatingField('status'),css_class="col-lg-6")
            )
        )
        # parent_ = kwargs.pop('parent_id', '')
        super(RadioForm, self).__init__(*args, **kwargs)
        # if parent_:
        #     self.initial['site'] = Site.objects.get(id=parent_)
        #     self.fields['site'].queryset = Site.objects.filter(id=parent_)
        #     self.fields['site'].required = True

    # def clean_code(self):
    #     code = self.cleaned_data['code']
    #     if not self.instance and BudgetItem.objects.filter(code=code).exists():
    #         raise ValidationError(f"Code already exists.")
    #     return code

    def get_cancel_url(self):
        return reverse('cit:radio-list')


class RadioLicenseForm(forms.ModelForm):

    class Meta:
        model = RadioLicense
        fields = ['license_number','radio', 'effective_date', 'expiry_date' ]

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('code'),css_class="col-lg-2"),
                Column(FloatingField('name'),css_class="col-lg-10")
            ),
            Row(
                Column(FloatingField('effective_date'),css_class="col-lg-2"),
                Column(FloatingField('expiry_date_date'),css_class="col-lg-10")
            )
        )
        super(RadioLicenseForm, self).__init__(*args, **kwargs)
    # def clean_code(self):
    #     code = self.cleaned_data['code']
    #     if not self.instance and Category.objects.filter(code=code).exists():
    #         raise ValidationError(f"Code already exists.")
    #     return code

    # def get_cancel_url(self):
    #     return reverse('project:budgetitem-list')
