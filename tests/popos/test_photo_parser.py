from django.test import TestCase
from api.popos.photo_parser import PhotoParser
from api.services.photo_service import PhotoService


class PhotoParserTest(TestCase):
    def setUp(self):
        location = 'san diego'
        results = PhotoService().get_single_photo_by_keyword(location)

        self.parser = PhotoParser(results, location)

    def test_it_exists(self):
        self.assertIsInstance(self.parser, PhotoParser)

    def test_attributes(self):
        self.assertIsInstance(self.parser.image_url, str)
        self.assertIsNotNone(self.parser.user_data)
        self.assertIsInstance(self.parser.location, str)

    def test_credit_info(self):
        self.assertEqual(self.parser.get_credit_info()['source'], 'unsplash.com')
        self.assertIsInstance(self.parser.get_credit_info()['author'], str)
        self.assertIsInstance(self.parser.get_credit_info()['logo'], str)

    def test_get_background_payload(self):
        self.assertEqual(self.parser.get_photo_payload()['data']['type'], 'image')
        self.assertIsNone(self.parser.get_photo_payload()['data']['id'])
        self.assertIsInstance(self.parser.get_photo_payload()['data']['image']['location'], str)
        self.assertIsInstance(self.parser.get_photo_payload()['data']['image']['image_url'], str)
        self.assertIsInstance(self.parser.get_photo_payload()['data']['image']['credit']['source'], str)
        self.assertIsInstance(self.parser.get_photo_payload()['data']['image']['credit']['author'], str)
        self.assertIsInstance(self.parser.get_photo_payload()['data']['image']['credit']['logo'], str)

