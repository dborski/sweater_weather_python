import os
import json
import requests
from django.test import TestCase
from api.services.location_service import get_latlng


class LocationService(TestCase):
  def test_get_geocoded_location(self):
    city = 'denver'
    state = 'co'

    results = get_latlng(city, state)

    self.assertIsInstance(results['lat'], float)
    self.assertIsInstance(results['lng'], float)
