# from __future__ import unicode_literals

import os
from django.conf import settings
from django import forms
from django.forms.widgets import ClearableFileInput

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group, Permission

from .models import Document, DocHeader
from .validators import validate_max_size
from crispy_forms.layout import Field, Column
from base.forms import Helper, SELECTFILTER_CSS
from django.contrib.admin.widgets import FilteredSelectMultiple


class DocumentForm(forms.ModelForm):
    document_file = forms.FileField(
        label=_('File'),
        validators=[validate_max_size],
        help_text='Maximum size of 5MB',
        widget=ClearableFileInput() # xxx
    )

    class Meta:
        model = Document
        fields = ('document_file',)

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Column(Field('document_file'),css_class="col-12")
        )
        super(DocumentForm, self).__init__(*args, **kwargs)

    def clean_document_file(self):
        file = self.cleaned_data.get('document_file', None)
        if not file:
            raise forms.ValidationError('Missing file')
        try:
            extension = os.path.splitext(file.name)[1][1:].lower()
            if extension in settings.FILE_UPLOAD_ALLOWED_TYPES:
                return file
            else:
                print('invalid_format')
                raise forms.ValidationError('File types is not allowed')
        except Exception:
            raise forms.ValidationError('Can not identify file type')

    def save(self, request, obj, *args, **kwargs):
        self.instance.creator = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.pk
        super(DocumentForm, self).save(*args, **kwargs)


class DocHeaderForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Group", is_stacked=False)
    )

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n', ]

    class Meta:
        model = DocHeader
        fields = ['name','groups']

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Field('name'),
            Field('groups')
        )
        super(DocHeaderForm, self).__init__(*args, **kwargs)
