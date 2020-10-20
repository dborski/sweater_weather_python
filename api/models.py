from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  api_key = models.CharField(max_length=60)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

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

class RoadTrip(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  start_city = models.CharField(max_length=30)
  end_city = models.CharField(max_length=30)
  travel_time = models.CharField(max_length=30)
  arrival_temp = models.FloatField()
  arrival_conditions = models.CharField(max_length=60)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
