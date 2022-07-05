from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User
from freelancer.resume.models import CV


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created=False, **kwargs):
    """
        sender: 
            Sender model from which you'll receive a signal.
        instance:
            Model instance(a record) which is saved(the actual instance being saved).
    """
    if created:
        Profile.objects.create(user=instance)
        CV.objects.create(user=instance)
    