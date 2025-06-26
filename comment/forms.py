from django import forms
from django.contrib.contenttypes.models import ContentType
from crispy_forms.layout import Field, Column
from base.forms import Helper, SELECTFILTER_CSS
# from django.utils.translation import ugettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Column(Field('message'),css_class="col-12")
        )
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, request, obj, *args, **kwargs):
        self.instance.created_by = request.user
        self.instance.updated_by = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.pk
        super(PostForm, self).save(*args, **kwargs)
