from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  api_key = models.CharField(max_length=60)

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
          user=instance, 
          api_key=str(uuid.uuid4())
        )

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
