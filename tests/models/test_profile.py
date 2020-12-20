from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1@email.com', email='user1@email.com', password='password')
        self.profile1 = self.user1.profile

    def test_string_representation(self):
        self.assertIsInstance(self.profile1.api_key, str)

    def test_relationship_user_and_profile(self):
        self.assertIsInstance(self.user1.profile.api_key, str)


