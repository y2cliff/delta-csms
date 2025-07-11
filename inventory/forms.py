from base.forms import Helper, SELECTFILTER_CSS, ClearableSelect2Widget
from crispy_forms.layout import Field, Row, Column, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from .models import InvCategory



class InvCategoryForm(forms.ModelForm):

    class Meta:
        model = InvCategory
        fields = ['code','name','description']

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
            Column(FloatingField('description'),css_class="col-lg-12")
            )
        )
        super(InvCategoryForm, self).__init__(*args, **kwargs)


    def clean_code(self):
        code = self.cleaned_data['code']
        if not self.instance and InvCategory.objects.filter(code=code).exists():
            raise forms.ValidationError(f"Code already exists.")
        return code

    def get_cancel_url(self):
        return reverse('inventory:invcategory-list')