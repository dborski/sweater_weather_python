import json
from django.test import TestCase

class GetForecastTest(TestCase):
  def test_get_weather_for_a_city(self):
    response = self.client.get('/api/v1/forecast?location=san diego,ca')

    json_response = response.json()

    self.assertEqual(response.status_code, 200)
    self.assertIsNotNone(json_response['data']['attributes']['current_weather'])
    self.assertIsNotNone(json_response['data']['attributes']['hourly_weather'])
    self.assertIsNotNone(json_response['data']['attributes']['daily_weather'])