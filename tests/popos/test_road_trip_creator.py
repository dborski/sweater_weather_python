from django.test import TestCase
from django.contrib.auth.models import User
from api.models import RoadTrip
from api.popos.road_trip_creator import RoadTripCreator
from api.services.location_service import get_directions


class RoadTripCreatorTest(TestCase):
  def setUp(self):
    self.start_location = 'denver,co'
    self.end_location = 'taos,nm'
    self.bad_end_location = 'london, uk'

    self.user1 = User.objects.create_user(
        username='user1@email.com', email='user1@email.com', password='password'
    )

    self.creator = RoadTripCreator(self.start_location, self.end_location, self.user1)
    self.creator_bad = RoadTripCreator(self.start_location, self.bad_end_location, self.user1)

  def test_it_exists(self):
    self.assertIsInstance(self.creator, RoadTripCreator)

  def test_attributes(self):
    self.assertEqual(self.creator.start_location, self.start_location)
    self.assertEqual(self.creator.end_location, self.end_location)
    self.assertIsNotNone(self.creator.directions)
    self.assertEqual(self.creator.user, self.user1)

  def test_happy_path_get_travel_time(self):
    self.assertIsInstance(self.creator.get_travel_time()[0], str)

  def test_sad_path_get_travel_time_that_is_impossible(self):
    self.assertEqual(self.creator_bad.get_travel_time(), 'Impossible')

  def test_happy_path_get_weather_at_eta(self):
    self.assertIsInstance(self.creator.get_weather_at_eta()['temperature'], float)
    self.assertIsInstance(self.creator.get_weather_at_eta()['conditions'], str)

  def test_sad_path_get_weather_at_eta_that_is_impossible(self):
    self.assertEqual(self.creator_bad.get_weather_at_eta()['temperature'], 'Impossible')
    self.assertEqual(self.creator_bad.get_weather_at_eta()['conditions'], 'Impossible')

  def test_happy_path_create_road_trip(self):
    self.creator.create_road_trip()

    road_trip = RoadTrip.objects.last()

    self.assertEqual(road_trip.start_city, 'denver,co')
    self.assertEqual(road_trip.end_city, 'taos,nm')
    self.assertIsInstance(road_trip.travel_time, str)
    self.assertIsNotNone(road_trip.arrival_temp)
    self.assertIsInstance(road_trip.arrival_conditions, str)