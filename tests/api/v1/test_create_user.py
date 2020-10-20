import json
from django.test import TestCase
from django.contrib.auth.models import User



class UserTest(TestCase):
  def test_happy_path_post_new_user(self):
    body = {
      'email': 'newuser@email.com',
      'password': 'password',
      'password_confirmation': 'password',
    }
    response = self.client.post('/api/v1/users', body)

    json_response = response.json()

    self.assertEqual(response.status_code, 201)
    self.assertEqual(json_response['data']['type'], 'users')
    self.assertIsInstance(json_response['data']['id'], int)
    self.assertEqual(json_response['data']['attributes']['email'], body['email'])
    self.assertIsInstance(json_response['data']['attributes']['api_key'], str)
