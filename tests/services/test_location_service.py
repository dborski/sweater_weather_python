from django.test import TestCase
from api.services.location_service import LocationService


class LocationServiceTest(TestCase):
    def setUp(self):
        self.service = LocationService()
  
    def test_get_geocoded_location(self):
        city = 'denver'
        state = 'co'

        results = self.service.get_latlng(city, state)

        self.assertIsInstance(results['lat'], float)
        self.assertIsInstance(results['lng'], float)

    def test_get_directions_from_to_location(self):
        start_location = 'Denver,CO'
        end_location = 'Taos,NM'

        results = self.service.get_directions(start_location, end_location).json()

        self.assertIsNotNone(results['route']['distance'])
        self.assertIsNotNone(results['route']['formattedTime'])