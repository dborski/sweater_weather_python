import json
from django.test import TestCase


class GetBackgroundImageTest(TestCase):
  def test_happy_path_get_background_image_for_city(self):
    response = self.client.get('/api/v1/backgrounds?location=san diego,ca')

    json_response = response.json()

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json_response['data']['type'], 'image')
    self.assertIsNone(json_response['data']['id'])
    self.assertIsNotNone(json_response['data']['image']['location'])
    self.assertIsNotNone(json_response['data']['image']['image_url'])
    self.assertIsNotNone(json_response['data']['image']['credit']['source'])
    self.assertIsNotNone(json_response['data']['image']['credit']['author'])
    self.assertIsNotNone(json_response['data']['image']['credit']['logo'])

  def test_sad_path_get_background_image_no_location(self):
    response = self.client.get('/api/v1/backgrounds')

    json_response = response.json()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json_response['success'], False)
    self.assertEqual(json_response['error'], 400)
    self.assertEqual(json_response['errors'], 'Must search query param /backgrounds?location=denver,co')

