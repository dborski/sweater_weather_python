from django.test import TestCase
from api.models import User

class UserModelTest(TestCase):
  def setUp(self):
    self.user1 = User.objects.create(username='user1@email.com', email='user1@email.com', password='password')

  def test_string_representation(self):
    self.assertEqual(str(self.user1), self.user1.username)


