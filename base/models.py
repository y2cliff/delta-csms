from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import F, Count, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class MenuQuerySet(models.query.QuerySet):
    def module_set(self, module):
        return self.filter(module=module)

    def my_menu(self, userprofile):
        return self.exclude(menu_type='Module').filter(user_profile=userprofile)


class MenuManager(models.Manager):
    def get_queryset(self):
        return MenuQuerySet(self.model, using=self._db)

    def module_set(self, module):
        return self.get_queryset().module_set(module=module).all()


class Menu(TemplateModel):
    MENU_TYPE = (
         ('Module', 'Module'),
         ('Parent', 'Parent'),
         ('Menu', 'Menu'),
         ('Label', 'Label'),
    )
    # sequence = models.PositiveIntegerField(default=0)
    module = models.CharField(max_length=60, blank=True, null=True)
    menu_type = models.CharField(max_length=10, default="Module", choices=MENU_TYPE)
    name = models.CharField(max_length=60, blank=True, null=True)
    url_name = models.CharField(max_length=60, blank=True, null=True)
    icon_class = models.CharField(max_length=60, blank=True, null=True)

    objects = MenuManager()

    class Meta:
        ordering = ['module','name']

    def __str__(self):
        if self.module:
            return 'Module: '+ self.module.title() + ' - Menu Name: ' + self.name + '_' + self.menu_type
        else:
            return self.name + '_' + self.menu_type

    def get_absolute_url(self):
        return reverse('menu-detail',kwargs={'pk': self.id})


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
    menu = models.ManyToManyField(Menu, through='UserMenuOrder', related_name='users')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'

    @property
    def get_full_name(self):
        return self.user.last_name + ',' + self.user.first_name

    def get_absolute_url(self):
        return reverse('userprofile-detail',kwargs={'pk': self.pk})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # if created:
    #     UserProfile.objects.create(user=instance)

    if created:
        # import inspect
        # for frame_record in inspect.stack():
        #     if frame_record[3] == 'get_response':
        #         request = frame_record[0].f_locals['request']
        #         break
        #     else:
        #         request = None
        if User.objects.all().count() > 1:
            UserProfile.objects.get_or_create(
                user=instance,
                created_by=get_current_user(),
                updated_by=get_current_user()
            )
        else:
            UserProfile.objects.get_or_create(
                user=instance,
                created_by_id=1,
                updated_by_id=1
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # instance.profile.save()

    # import inspect
    # for frame_record in inspect.stack():
    #     if frame_record[3] == 'get_response':
    #         request = frame_record[0].f_locals['request']
    #         break
    #     else:
    #         request = None
    if User.objects.all().count() > 1:
        instance.profile.updated_by = get_current_user()
        instance.profile.save()


class MenuManager(models.Manager):
    def get_queryset(self):
        return MenuQuerySet(self.model, using=self._db)

    def module_set(self, module):
        return self.get_queryset().module_set(module=module).all()

    def my_module_menus(self, module, user):
        return self.get_queryset().module_set(module=module).all()


class UserMenuQuerySet(models.query.QuerySet):
    def my_module_menus(self, module, user):
        return self.filter(menu__module=module, userprofile__user=user)


class UserMenuManager(models.Manager):
    def get_queryset(self):
        return UserMenuQuerySet(self.model, using=self._db)

    def my_module_menus(self, module, user):
        return self.get_queryset().my_module_menus(module=module, user=user).all()


class UserMenuOrder(TemplateModel):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    objects = UserMenuManager()

    class Meta:
        ordering = ['order']
        unique_together = ('userprofile', 'menu', 'order')

    def __str__(self):
        return f"User: {self.userprofile} - Menu: {self.menu} (Order: {self.order})"

    def get_absolute_url(self):
        return reverse('userprofile-detail',kwargs={'pk': self.userprofile.pk})

# -----------------------------------------------------
# PROJECT ACCESS RESTRICTION
# 
# -----------------------------------------------------

# class GroupProfile(Group):
#     class Meta:
#         proxy = True

#     def get_absolute_url(self):
#         return reverse('xystum:groupprofile-detail', kwargs={'id': self.id})

#     def has_access(self):
#         access = Access.objects.filter(group=self.id).exists()
#         return access
