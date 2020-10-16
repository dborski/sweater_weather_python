import os
import json
import requests
from django.test import TestCase
from api.services.photo_service import get_photos_by_keyword, get_single_photo_by_keyword
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class WeatherService(TestCase):
  def setUp(self):
    search_query = 'denver'

    self.results = get_photos_by_keyword(search_query).json()
    self.single_result = get_single_photo_by_keyword(search_query)

  def test_get_photos_by_keyword(self):
    self.assertIsInstance(self.results['results'], list)
    self.assertIsNotNone(self.results['results'][0]['width'])
    self.assertIsNotNone(self.results['results'][0]['height'])
    self.assertIsNotNone(self.results['results'][0]['urls'])
    self.assertIsNotNone(self.results['results'][0]['links'])
    self.assertIsNotNone(self.results['results'][0]['user'])

  def test_get_single_photo_by_keyword(self):
    self.assertIsNotNone(self.single_result['width'])
    self.assertIsNotNone(self.single_result['height'])
    self.assertIsNotNone(self.single_result['urls'])
    self.assertIsNotNone(self.single_result['links'])
    self.assertIsNotNone(self.single_result['user'])
