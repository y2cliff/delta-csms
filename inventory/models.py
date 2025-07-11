from base.abstract import TemplateModel
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class InvCategory(TemplateModel):
    code = models.CharField(
        max_length=10, 
        unique=True, 
        error_messages={'unique': "Code has already been used."}
    )
    name = models.CharField(max_length=60, blank=True, null=True)
    description = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ["code"]
        permissions = (
            ('delete_foreign_Category', _('Can delete foreign Category')),
        )

    def __str__(self):
        return self.code + ' - ' + self.name

    def get_absolute_url(self):
        return reverse('inventory:invcategory-detail',kwargs={'pk': self.id})