from django.test import TestCase
from api.popos.photo_parser import PhotoParser
from api.services.photo_service import get_single_photo_by_keyword


class PhotoParserTest(TestCase):
  def setUp(self):
    location = 'san diego'
    results = get_single_photo_by_keyword(location)

    self.parser = PhotoParser(results, location)

  def test_it_exists(self):
    self.assertIsInstance(self.parser, PhotoParser)
  
  def test_attributes(self):
    self.assertIsInstance(self.parser.image_url, str)
    self.assertIsNotNone(self.parser.user_data)
    self.assertIsInstance(self.parser.location, str)