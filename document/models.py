# from __future__ import unicode_literals
# from six import python_2_unicode_compatible

import os

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.abstract import TemplateModel


def document_upload(instance, filename):
    """Stores the document in a "per module/appname/primary key" folder"""
    return 'documents/{app}_{model}/{pk}/{filename}'.format(
        app=instance.content_object._meta.app_label,
        model=instance.content_object._meta.object_name.lower(),
        pk=instance.content_object.pk,
        filename=filename,
    )


class DocumentManager(models.Manager):
    def documents_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id, object_id=obj.pk)


# @python_2_unicode_compatible
class Document(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_documents",
        verbose_name=_('creator'),
        on_delete=models.CASCADE,
    )
    document_file = models.FileField(
        _('document'), upload_to=document_upload
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    objects = DocumentManager()

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ['-created']
        permissions = (
            ('delete_foreign_documents', _('Can delete foreign documents')),
        )

    def __str__(self):
        return _('{username} attached {filename}').format(
            username=self.creator.get_username(),
            filename=self.document_file.name,
        )

    @property
    def filename(self):
        return os.path.split(self.document_file.name)[1]


class DocumentHome(TemplateModel):
    def get_absolute_url(self):
        return reverse("document:home")


class DocHeader(TemplateModel):
    name = models.CharField(max_length=30)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('document:docheader-detail', kwargs={'id': self.id})
