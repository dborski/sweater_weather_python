import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from api.services.location_service import get_latlng
from api.services.weather_service import get_forecast
from api.services.photo_service import get_photos_by_keyword, get_single_photo_by_keyword

class GetForecastTest(TestCase):
  def test_get_weather_for_a_city(self):
    params = {'location': 'denver,co'}
    response = self.client.get('/api/v1/forecast', params=params)

    self.assertEqual(response.status_code, 200)