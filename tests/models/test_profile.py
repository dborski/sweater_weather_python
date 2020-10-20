from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Profile

class ProfileModelTest(TestCase):
  def setUp(self):
    self.user1 = User.objects.create_user(username='user1@email.com', email='user1@email.com', password='password')
    self.profile1 = Profile.objects.create(user=self.user1.id, api_key="1234-5678")

  def test_string_representation(self):
    self.assertEqual(self.profile1.api_key, "1234-5678")


