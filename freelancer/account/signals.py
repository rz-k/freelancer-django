import os

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from freelancer.pricing.models import ActivePricingPanel, PricingPanel
from freelancer.resume.models import CV

from .models import Profile, User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created=False, **kwargs):
    """
        Sender:
            Sender model from which you'll receive a signal.
        Instance:
            Model instance(a record) which is saved(the actual instance being saved).
    """
    if created:
        # Create a Default Profile.
        Profile.objects.create(user=instance)

        # Create a Default Resome.
        CV.objects.create(user=instance)

        # Create a Default Pricing panel.
        ActivePricingPanel.objects.create(
            user=instance,
            active_panel=PricingPanel.objects.get(position=0))


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
