from django.contrib.auth.models import User, Group
from django.db import models
# from django.db.models import F, Count, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .abstract import GetOrNoneManager, TemplateModel
from django_currentuser.middleware import get_current_user, get_current_authenticated_user


def image_upload(instance, filename):
    """Stores the document in a "per module/appname/primary key" folder"""
    return 'img/{app_label}/{model_name}/{pk}/{filename}'.format(
        app_label=instance._meta.app_label,
        model_name=instance._meta.model_name,
        pk=instance.pk,
        filename=filename,
    )

def get_user_menus(user):
    if user.is_superuser:
        return Menu.objects.all()
    direct_menus = list(user.profile.menu.all())
    group_menus = list(Menu.objects.filter(
        groups__in=GroupProfile.objects.filter(
            group__in=user.groups.all())))
    combined = {menu.id: menu for menu in direct_menus + group_menus }
    sorted_menus = sorted(combined.values(), key=lambda m: m.code.lower())
    return sorted_menus

class Menu(TemplateModel):
    MENU_TYPE = (
         ('Module', 'Module'),
         ('Parent', 'Parent'),
         ('Menu', 'Menu'),
         ('Label', 'Label'),
    )
    code = models.CharField(max_length=8, blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    menu_type = models.CharField(max_length=10, default="Module", choices=MENU_TYPE)
    name = models.CharField(max_length=60, blank=True, null=True)
    url_name = models.CharField(max_length=60, blank=True, null=True)
    icon_class = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        if self.module:
            return self.code + ' - ' + self.name + ' - ' + self.menu_type
        else:
            return self.name + '_' + self.menu_type

    def get_absolute_url(self):
        return reverse('menu-detail',kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = 'ZZZZ-999'
        super().save(*args, **kwargs)

class UserProfile(TemplateModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    about = models.TextField(default="", blank=True)
    company = models.CharField(max_length=60, blank=True, null=True)
    job = models.CharField(max_length=60, blank=True, null=True)
    country = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    image_file = models.ImageField(
        _('image'), upload_to=image_upload, height_field='image_height', width_field='image_width', blank=True, null=True
    )
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    twitter = models.CharField(max_length=60, blank=True, null=True)
    facebook = models.CharField(max_length=60, blank=True, null=True)
    instagram = models.CharField(max_length=60, blank=True, null=True)
    linkedin = models.CharField(max_length=60, blank=True, null=True)
    menu = models.ManyToManyField(
        Menu,
        blank=True,
        symmetrical=False,
        related_name='users'
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'

    @property
    def get_full_name(self):
        return self.user.last_name + ',' + self.user.first_name

    def get_absolute_url(self):
        return reverse('userprofile-detail',kwargs={'pk': self.pk})

class Department(TemplateModel):
    code = models.CharField(max_length=60, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Department'

    def get_absolute_url(self):
        return reverse('department-detail',kwargs={'pk': self.id})

class GroupProfile(TemplateModel):
    group = models.OneToOneField(
        Group, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    name = models.CharField(max_length=60, blank=True, null=True)
    menu = models.ManyToManyField(
        Menu,
        blank=True,
        symmetrical=False,
        related_name='groups'
    )

    def __str__(self):
        name_ = self.group.name
        if self.name:
            name_ = self.name
        return name_

    class Meta:
        verbose_name = 'Group Profile'

    def get_absolute_url(self):
        return reverse('groupprofile-detail',kwargs={'pk': self.pk})
