import os

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from freelancer.resume.models import CV

from .models import Profile, User
from freelancer.pricing.models import ActivePricingPanel, PricingPanel


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created=False, **kwargs):
    """
        Sender:
            Sender model from which you'll receive a signal.
        Instance:
            Model instance(a record) which is saved(the actual instance being saved).
    """
    if created:
        Profile.objects.create(user=instance)
        CV.objects.create(user=instance)
        
        ActivePricingPanel.objects.create(
            user=instance, 
            active_panel=PricingPanel.objects.first(),
            )
        


@receiver(pre_save, sender=Profile)
def delete_old_avatar(sender, instance, **kwargs):
    """
    Remove the oldest avatar image before adding a new one.
    """
    try:
        old_avatar = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False

    new_avatar = instance.avatar
    if old_avatar != new_avatar:
        if old_avatar and os.path.isfile(old_avatar.path) and os.path.exists(old_avatar.path):
            os.remove(old_avatar.path)
