from django.dispatch import receiver
from django.db.models.signals import post_save

from useraccount.models import UserAccount
from .models import ProfilePage
from business.models import Business


@receiver(post_save, sender=UserAccount)
def create_profile_user(instance, created, **kwargs):
    if created:
        ProfilePage.objects.create(subject=instance)
        
@receiver(post_save, sender=Business)
def create_profile_business(instance, created, **kwargs):
    if created:
        ProfilePage.objects.create(subject=instance)