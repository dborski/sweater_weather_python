# import os
# import json
# import requests
# from django.test import TestCase
# from api.services.location_service import get_latlng, get_directions


# class LocationService(TestCase):
#   def test_get_geocoded_location(self):
#     city = 'denver'
#     state = 'co'

#     results = get_latlng(city, state)

#     self.assertIsInstance(results['lat'], float)
#     self.assertIsInstance(results['lng'], float)

#   def test_get_directions_from_to_location(self):
#     start_location = 'Denver,CO'
#     end_location = 'Taos,NM'

#     results = get_directions(start_location, end_location).json()

#     self.assertIsNotNone(results['route']['distance'])
#     self.assertIsNotNone(results['route']['formattedTime'])
