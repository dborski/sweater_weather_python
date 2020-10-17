from django.test import TestCase
from api.popos.forecast_parser import ForecastParser
from api.services.weather_service import get_forecast


class ForecastParserTest(TestCase):
  def setUp(self):
    self.lat = '39.738453'
    self.lng = '-104.984853'
    self.exclude = 'minutely'

    self.results = get_forecast(self.lat, self.lng, self.exclude).json()

    self.parser = ForecastParser(self.results)

  def test_it_exists(self):
    self.assertIsInstance(self.parser, ForecastParser)

  def test_attributes(self):
    self.assertIsInstance(self.parser.current, dict)
    self.assertIsInstance(self.parser.hourly, list)
    self.assertIsInstance(self.parser.daily, list)

  def test_parse_current_weather(self):
    self.assertIsInstance(self.parser.parse_current_weather()['datetime'], str)
    self.assertIsInstance(self.parser.parse_current_weather()['sunrise'], str)
    self.assertIsInstance(self.parser.parse_current_weather()['sunset'], str)
    self.assertIsInstance(self.parser.parse_current_weather()['temperature'], float)
    self.assertIsInstance(self.parser.parse_current_weather()['feels_like'], float)
    self.assertIsInstance(self.parser.parse_current_weather()['humidity'], int)
    self.assertIsNotNone(self.parser.parse_current_weather()['uvi'])
    self.assertIsInstance(self.parser.parse_current_weather()['visibility'], int)
    self.assertIsInstance(self.parser.parse_current_weather()['conditions'], str)
    self.assertIsInstance(self.parser.parse_current_weather()['icon'], str)

