import os
from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


def validate_max_size(data):
    if (
        hasattr(settings, 'FILE_UPLOAD_MAX_SIZE') and
        data.size > settings.FILE_UPLOAD_MAX_SIZE
    ):
        raise forms.ValidationError(
            _('File exceeds maximum size of {size}').format(
                size=filesizeformat(settings.FILE_UPLOAD_MAX_SIZE)
            )
        )

def validate_type(data):
    extension = os.path.splitext(data.name)[1][1:].lower()
    if extension not in settings.FILE_UPLOAD_ALLOWED_TYPES:
        raise forms.ValidationError('File types is not allowed')
