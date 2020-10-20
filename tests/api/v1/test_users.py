import json
from django.test import TestCase
from django.contrib.auth.models import User


class UserRegistrationTest(TestCase):
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

  def test_sad_path_post_user_with_passwords_that_dont_match(self):
    body = {
      'email': 'new_user@email.com',
      'password': 'password',
      'password_confirmation': 'password34',
    }
    response = self.client.post('/api/v1/users', body)

    json_response = response.json()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json_response['success'], False)
    self.assertEqual(json_response['error'], 400)
    self.assertEqual(json_response['errors'], 'The passwords do not match')

  def test_sad_path_post_user_with_missing_email(self):
    body = {
      'password': 'password',
      'password_confirmation': 'password34',
    }
    response = self.client.post('/api/v1/users', body)

    json_response = response.json()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json_response['success'], False)
    self.assertEqual(json_response['error'], 400)
    self.assertEqual(json_response['errors'], 'Missing email')

  def test_sad_path_post_user_with_missing_password(self):
    body = {
      'email': 'new_user@email.com',
      'password_confirmation': 'password34',
    }
    response = self.client.post('/api/v1/users', body)

    json_response = response.json()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json_response['success'], False)
    self.assertEqual(json_response['error'], 400)
    self.assertEqual(json_response['errors'], 'Missing password')

  def test_sad_path_post_user_with_missing_password_confirmation(self):
    body = {
      'email': 'new_user@email.com',
      'password': 'password34',
    }
    response = self.client.post('/api/v1/users', body)

    json_response = response.json()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json_response['success'], False)
    self.assertEqual(json_response['error'], 400)
    self.assertEqual(json_response['errors'], 'Missing password confirmation')

class UserLoginTest(TestCase):
  def setUp(self):
    self.user1 = User.objects.create_user(
        username='currentuser1@email.com',
        email='currentuse1r@email.com',
        password='password1'
    )

    self.user2 = User.objects.create_user(
        username='currentuser2@email.com',
        email='currentuse2r@email.com',
        password='password2'
    )
  
  def test_happy_path_logs_in_a_user(self):
    body = {
      'email': 'currentuser2@email.com',
      'password': 'password2',
    }
    response = self.client.post('/api/v1/sessions', body)

    json_response = response.json()

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json_response['data']['type'], 'users')
    self.assertEqual(json_response['data']['id'], self.user2.id)
    self.assertEqual(json_response['data']['attributes']['email'], self.user2.email)
    self.assertEqual(json_response['data']['attributes']['api_key'], self.user2.profile.api_key)
