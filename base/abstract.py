from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import get_current_user
from django.utils.timezone import now


User = get_user_model()

class TemplateModel(models.Model):
    # CHOICES
    # DATABASE FIELDS
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = CurrentUserField(related_name="%(class)s_created", on_update=False)
    updated_by = CurrentUserField(related_name="%(class)s_updated", on_update=True)
    # MANAGERS
    # META CLASS
    class Meta:
        abstract = True
    # TO STRING METHOD
    # SAVE METHOD
    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = now()
            self.created_by = get_current_user()
        self.date_updated = now()
        # self.updated_by =get_current_user()
        super().save(*args, **kwargs)
    # ABSOLUTE URL METHOD
    # OTHER METHODS


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

