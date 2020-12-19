# import json
# from django.test import TestCase

# class GetForecastTest(TestCase):
#   def test_happy_path_get_weather_for_a_city(self):
#     response = self.client.get('/api/v1/forecast?location=san diego,ca')

#     json_response = response.json()

#     self.assertEqual(response.status_code, 200)
#     self.assertIsNotNone(json_response['data']['attributes']['current_weather'])
#     self.assertIsNotNone(json_response['data']['attributes']['hourly_weather'])
#     self.assertIsNotNone(json_response['data']['attributes']['daily_weather'])

#   def test_sad_path_get_weather_no_state(self):
#     response = self.client.get('/api/v1/forecast?location=san diego')

#     json_response = response.json()

#     self.assertEqual(response.status_code, 400)
#     self.assertEqual(json_response['success'], False)
#     self.assertEqual(json_response['error'], 400)
#     self.assertEqual(json_response['errors'], 'Must include city and state ex. /forecast?location=denver,co')

#   def test_sad_path_get_weather_no_city(self):
#     response = self.client.get('/api/v1/forecast?location=ca')

#     json_response = response.json()

#     self.assertEqual(response.status_code, 400)
#     self.assertEqual(json_response['success'], False)
#     self.assertEqual(json_response['error'], 400)
#     self.assertEqual(json_response['errors'], 'Must include city and state ex. /forecast?location=denver,co')
