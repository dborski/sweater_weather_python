from django.test import TestCase
from api.popos.forecast_parser import ForecastParser
from api.services.weather_service import WeatherService


class ForecastParserTest(TestCase):
    def setUp(self):
        self.lat = '39.738453'
        self.lng = '-104.984853'
        self.exclude = 'minutely'

        self.results = WeatherService().get_forecast(self.lat, self.lng, self.exclude).json()

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
        self.assertIsNotNone(self.parser.parse_current_weather()['temperature'])
        self.assertIsNotNone(self.parser.parse_current_weather()['feels_like'])
        self.assertIsInstance(self.parser.parse_current_weather()['humidity'], int)
        self.assertIsNotNone(self.parser.parse_current_weather()['uvi'])
        self.assertIsInstance(self.parser.parse_current_weather()['visibility'], int)
        self.assertIsInstance(self.parser.parse_current_weather()['conditions'], str)
        self.assertIsInstance(self.parser.parse_current_weather()['icon'], str)

    def test_parse_hourly_weather(self):
        self.assertEqual(len(self.parser.parse_hourly_weather()), 8)
        self.assertIsInstance(self.parser.parse_hourly_weather()[0]['time'], str)
        self.assertIsNotNone(self.parser.parse_hourly_weather()[0]['temp'])
        self.assertIsInstance(self.parser.parse_hourly_weather()[0]['wind_speed'], str)
        self.assertIsInstance(self.parser.parse_hourly_weather()[0]['wind_direction'], str)
        self.assertIsInstance(self.parser.parse_hourly_weather()[0]['conditions'], str)
        self.assertIsInstance(self.parser.parse_hourly_weather()[0]['icon'], str)

    def test_parse_daily_weather(self):
        self.assertEqual(len(self.parser.parse_daily_weather()), 5)
        self.assertIsInstance(self.parser.parse_daily_weather()[0]['date'], str)
        self.assertIsInstance(self.parser.parse_daily_weather()[0]['sunrise'], str)
        self.assertIsInstance(self.parser.parse_daily_weather()[0]['sunset'], str)
        self.assertIsNotNone(self.parser.parse_daily_weather()[0]['max_temp'])
        self.assertIsNotNone(self.parser.parse_daily_weather()[0]['min_temp'])
        self.assertIsInstance(self.parser.parse_daily_weather()[0]['conditions'], str)
        self.assertIsInstance(self.parser.parse_daily_weather()[0]['icon'], str)

    def test_get_forecast_payload(self):
        self.assertEqual(self.parser.get_forecast_payload()['data']['type'], 'forecast')
        self.assertIsInstance(self.parser.get_forecast_payload()['data']['attributes']['current_weather']['datetime'], str)
        self.assertIsInstance(self.parser.get_forecast_payload()['data']['attributes']['hourly_weather'][0]['time'], str)
        self.assertIsInstance(self.parser.get_forecast_payload()['data']['attributes']['daily_weather'][0]['date'], str)


