from django.test import TestCase
from api.services.weather_service import get_forecast


class WeatherService(TestCase):
  def setUp(self):
    self.lat = '39.738453'
    self.lng = '-104.984853'
    self.exclude = 'minutely'

    self.results = get_forecast(self.lat, self.lng, self.exclude).json()


  def test_get_current_weather_for_location(self):
    self.assertIsNotNone(self.results['current'])
    self.assertIsInstance(self.results['current']['dt'], int)
    self.assertIsInstance(self.results['current']['sunrise'], int)
    self.assertIsInstance(self.results['current']['sunset'], int)
    self.assertIsNotNone(self.results['current']['temp'])
    self.assertIsInstance(self.results['current']['feels_like'], float)
    self.assertIsInstance(self.results['current']['pressure'], int)
    self.assertIsInstance(self.results['current']['humidity'], int)
    self.assertIsInstance(self.results['current']['dew_point'], float)
    self.assertIsInstance(self.results['current']['uvi'], float)
    self.assertIsInstance(self.results['current']['clouds'], int)
    self.assertIsInstance(self.results['current']['visibility'], int)
    self.assertIsNotNone(self.results['current']['wind_speed'])
    self.assertIsInstance(self.results['current']['wind_deg'], int)
    self.assertIsNotNone(self.results['current']['weather'][0]['main'])
    self.assertIsNotNone(self.results['current']['weather'][0]['description'])
    self.assertIsNotNone(self.results['current']['weather'][0]['icon'])

  def test_get_hourly_weather_for_location(self):
    self.assertIsNotNone(self.results['hourly'])
    self.assertIsInstance(self.results['hourly'][0]['dt'], int)
    self.assertIsNotNone(self.results['hourly'][0]['temp'])
    self.assertIsNotNone(self.results['hourly'][0]['feels_like'])
    self.assertIsInstance(self.results['hourly'][0]['pressure'], int)
    self.assertIsInstance(self.results['hourly'][0]['humidity'], int)
    self.assertIsInstance(self.results['hourly'][0]['dew_point'], float)
    self.assertIsInstance(self.results['hourly'][0]['clouds'], int)
    self.assertIsInstance(self.results['hourly'][0]['visibility'], int)
    self.assertIsNotNone(self.results['hourly'][0]['wind_speed'])
    self.assertIsInstance(self.results['hourly'][0]['wind_deg'], int)
    self.assertIsNotNone(self.results['hourly'][0]['weather'][0]['main'])
    self.assertIsNotNone(self.results['hourly'][0]['weather'][0]['description'])
    self.assertIsNotNone(self.results['hourly'][0]['weather'][0]['icon'])


  def test_get_daily_weather_for_location(self):
    self.assertIsInstance(self.results['daily'], list)
    self.assertIsInstance(self.results['daily'][0]['dt'], int)
    self.assertIsInstance(self.results['daily'][0]['sunrise'], int)
    self.assertIsInstance(self.results['daily'][0]['sunset'], int)
    self.assertIsNotNone(self.results['daily'][0]['temp'])
    self.assertIsNotNone(self.results['daily'][0]['feels_like'])
    self.assertIsInstance(self.results['daily'][0]['pressure'], int)
    self.assertIsInstance(self.results['daily'][0]['humidity'], int)
    self.assertIsInstance(self.results['daily'][0]['dew_point'], float)
    self.assertIsInstance(self.results['daily'][0]['wind_speed'], float)
    self.assertIsInstance(self.results['daily'][0]['wind_deg'], int)
    self.assertIsNotNone(self.results['daily'][0]['weather'][0]['main'])
    self.assertIsNotNone(self.results['daily'][0]['weather'][0]['description'])
    self.assertIsNotNone(self.results['daily'][0]['weather'][0]['icon'])
    self.assertIsInstance(self.results['daily'][0]['clouds'], int)
    self.assertIsInstance(self.results['daily'][0]['uvi'], float)


