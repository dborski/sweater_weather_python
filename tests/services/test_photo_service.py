from django.test import TestCase
from api.services.photo_service import PhotoService


class PhotoServiceTest(TestCase):
    def setUp(self):
        search_query = 'denver'

        self.service = PhotoService()

        self.results = self.service.get_photos_by_keyword(search_query).json()
        self.single_result = self.service.get_single_photo_by_keyword(search_query)

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
