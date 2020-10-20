from django.db import models


class User(models.Model):
  username = models.CharField(max_length=30)
  email = models.CharField(max_length=30)
  password = models.CharField(max_length=120)
  api_key = models.CharField(max_length=60)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.username
