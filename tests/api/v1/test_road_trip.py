import json
from django.test import TestCase
from django.contrib.auth.models import User


class GetRoadTripTest(TestCase):
  def test_happy_path_create_road_trip_for_user(self):
    self.user1 = User.objects.create_user(
        username='currentuser@email.com',
        email='currentuser@email.com',
        password='password'
    )
    body = {
        "origin": "Denver,CO",
        "destination": "Taos,NM",
        "api_key": self.user1.profile.api_key
    }

    response = self.client.post('/api/v1/road_trip', body)

    json_response = response.json()

    self.assertEqual(response.status_code, 201)
    self.assertIsNone(json_response['data']['id'])
    self.assertEqual(json_response['data']['id'], 'roadtrip')
    self.assertEqual(json_response['data']['attributes']['start_city'], body['origin'])
    self.assertEqual(json_response['data']['attributes']['end_city'], body['destination'])
    self.assertIsNotNone(json_response['data']['attributes']['travel_time'])
    self.assertIsNotNone(json_response['data']['attributes']['weather_at_eta']['temperature'])
    self.assertIsInstance(json_response['data']['attributes']['weather_at_eta']['conditions'], str)
