import json
from django.test import TestCase
from django.contrib.auth.models import User



class UserTest(TestCase):
  def setUp(self):
    self.user1 = User.objects.create_user(
      username='currentuser@email.com',
      email='currentuser@email.com',
      password='password'
    )

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

  def test_sad_path_post_user_with_repeat_email(self):
    body = {
      'email': 'currentuser@email.com',
      'password': 'password',
      'password_confirmation': 'password',
    }
    response = self.client.post('/api/v1/users', body)

    json_response = response.json()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json_response['success'], False)
    self.assertEqual(json_response['error'], 400)
    self.assertEqual(json_response['errors'], 'This email already exists')

