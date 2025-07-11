from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile, GroupProfile
from django_currentuser.middleware import get_current_user, get_current_authenticated_user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
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

@receiver(post_save, sender=Group)
def create_group_profile(sender, instance, created, **kwargs):
    if created:

        if Group.objects.all().count() > 1:
            GroupProfile.objects.get_or_create(
                group=instance,
                created_by=get_current_user(),
                updated_by=get_current_user()
            )
        else:
            GroupProfile.objects.get_or_create(
                group=instance,
                created_by_id=1,
                updated_by_id=1
            )

@receiver(post_save, sender=Group)
def save_group_profile(sender, instance, **kwargs):
    if Group.objects.all().count() > 1:
        instance.profile.updated_by = get_current_user()
        instance.profile.save()
