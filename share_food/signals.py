from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.conf import settings
from .models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def delete_profile_for_deleted_user(sender, **kwargs):
    try:
        userprofile = UserProfile.objects.get(user=kwargs['instance'])
        userprofile.delete()
    except UserProfile.DoesNotExist:
        pass
