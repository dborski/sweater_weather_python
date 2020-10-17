from django.test import TestCase
from api.popos import ForecastParser

class ForecastParserTest(TestCase):
  def setUp(self):
    payload = {"lat": 39.74,
               "lon": -104.98,
               "timezone": "America/Denver",
               "timezone_offset": -21600,
               "current": {},
               "hourly": {},
               "daily": {}
    }

    self.parser = ForecastParser(payload)

  def test_it_exists(self):
    self.assertIsInstance(self.parser, ForecastParser)

  def test_attributse(self):
    self.assertIsInstance(self.parser.current, dict)
    self.assertIsInstance(self.parser.hourly, dict)
    self.assertIsInstance(self.parser.daily, dict)

  def test_forecast_payload(self):
    expected = {}
    self.assertEqual()

