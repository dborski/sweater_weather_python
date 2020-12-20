from django.test import TestCase
from django.contrib.auth.models import User


class GetRoadTripTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='currentuser@email.com',
            email='currentuser@email.com',
            password='password'
        )

    def test_happy_path_create_road_trip_for_user(self):
        body = {
            "origin": "Denver,CO",
            "destination": "Taos,NM",
            "api_key": self.user1.profile.api_key
        }

        response = self.client.post('/api/v1/road_trip', body)

        json_response = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIsNone(json_response['data']['id'])
        self.assertEqual(json_response['data']['attributes']['start_city'], body['origin'])
        self.assertEqual(json_response['data']['attributes']['end_city'], body['destination'])
        self.assertIsNotNone(json_response['data']['attributes']['travel_time'])
        self.assertIsNotNone(json_response['data']['attributes']['weather_at_eta']['temperature'])
        self.assertIsInstance(json_response['data']['attributes']['weather_at_eta']['conditions'], str)

    def test_sad_path_api_key_missing(self):
        body = {
            "origin": "Denver,CO",
            "destination": "Taos,NM",
        }

        response = self.client.post('/api/v1/road_trip', body)

        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['error'], 400)
        self.assertEqual(json_response['errors'], "Must include api_key")

    def test_sad_path_origin_missing(self):
        body = {
            "destination": "Taos,NM",
            "api_key": self.user1.profile.api_key
        }

        response = self.client.post('/api/v1/road_trip', body)

        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['error'], 400)
        self.assertEqual(json_response['errors'], "Must include origin")

    def test_sad_path_destination_missing(self):
        body = {
            "origin": "Denver,CO",
            "api_key": self.user1.profile.api_key
        }

        response = self.client.post('/api/v1/road_trip', body)

        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['error'], 400)
        self.assertEqual(json_response['errors'], "Must include destination")

    def test_sad_path_impossible_route(self):
        body = {
            "origin": "Denver,CO",
            "destination": "London,UK",
            "api_key": self.user1.profile.api_key
        }

        response = self.client.post('/api/v1/road_trip', body)

        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIsNone(json_response['data']['id'])
        self.assertEqual(json_response['data']['attributes']['start_city'], body['origin'])
        self.assertEqual(json_response['data']['attributes']['end_city'], body['destination'])
        self.assertEqual(json_response['data']['attributes']['travel_time'], 'Impossible')
        self.assertIsNone(json_response['data']['attributes']['weather_at_eta'])

    def test_sad_path_trip_longer_than_48_hours(self):
        body = {
            "origin": "Denver,CO",
            "destination": "Managua,Nicaragua",
            "api_key": self.user1.profile.api_key
        }

        response = self.client.post('/api/v1/road_trip', body)

        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIsNone(json_response['data']['id'])
        self.assertEqual(json_response['data']['attributes']['start_city'], body['origin'])
        self.assertEqual(json_response['data']['attributes']['end_city'], body['destination'])
        self.assertEqual(json_response['data']['attributes']['travel_time'], 'Impossible')
        self.assertIsNone(json_response['data']['attributes']['weather_at_eta'])
