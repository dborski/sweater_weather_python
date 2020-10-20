from django.test import TestCase
from django.contrib.auth.models import User
from api.popos.road_trip_creator import RoadTripCreator
from api.services.location_service import get_directions


class RoadTripCreatorTest(TestCase):
  def setUp(self):
    self.start_location = 'denver,co'
    self.end_location = 'taos,nm'

    self.user1 = User.objects.create_user(
        username='user1@email.com', email='user1@email.com', password='password'
    )

    self.creator = RoadTripCreator(self.start_location, self.end_location, self.user1)

  def test_it_exists(self):
    self.assertIsInstance(self.creator, RoadTripCreator)

  def test_attributes(self):
    self.assertEqual(self.creator.start_location, self.start_location)
    self.assertEqual(self.creator.end_location, self.end_location)
    self.assertIsNotNone(self.creator.directions)
    self.assertEqual(self.creator.user, self.user1)


