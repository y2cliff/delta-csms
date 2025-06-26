from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.text import Truncator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class PostManager(models.Manager):
    def posts_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id, object_id=obj.pk)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    topic = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_posts",
        verbose_name=_('post_creator'),
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="+",
        verbose_name=_('post_updator'),
        on_delete=models.CASCADE,
    )

    objects = PostManager()

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ['created_at']
        permissions = (
            ('delete_foreign_posts', _('Can delete foreign posts')),
        )

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
