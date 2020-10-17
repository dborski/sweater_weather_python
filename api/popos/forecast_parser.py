# import pytz
from pytz import timezone
from datetime import datetime
import time

def _forecast_payload(forecast):
  return {
      "data": {
          "id": None,
          "type": "forecast",
          "attributes": {
              "current_weather": None,
              "daily_weather": None,
              "hourly_weather": None
          }
      }
  }

def covert_to_localtime(utctime, local_timezone):
  format = '%Y-%m-%d %H:%M:%S %z'
  local_time = time.strftime(format, time.localtime(int(utctime)))
  datetime_obj = datetime.strptime(local_time, format)
  datetime_new_tz = datetime_obj.replace(tzinfo=timezone(local_timezone))

  return datetime_new_tz.strftime(format)


class ForecastParser:
  def __init__(self, forecast):
    self.timezone = forecast['timezone']
    self.timezone_offset = forecast['timezone_offset']
    self.current = forecast['current']
    self.hourly = forecast['hourly']
    self.daily = forecast['daily']

  def parse_current_weather(self):
    return {
            "datetime": covert_to_localtime(self.current['dt'], self.timezone),
            "sunrise": covert_to_localtime(self.current['sunrise'], self.timezone),
            "sunset": covert_to_localtime(self.current['sunset'], self.timezone),
            "temperature": self.current['temp'],
            "feels_like": self.current['feels_like'],
            "humidity": self.current['humidity'],
            "uvi": self.current['uvi'],
            "visibility": self.current['visibility'],
            "conditions": self.current['weather'][0]['description'],
            "icon": self.current['weather'][0]['icon']
    }

  def parse_hourly_weather(self):
    payload = [
        {
            "time": "14:00:00",
            "wind_speed": "4 mph",
            "wind_direction": "from NW",
            "conditions": 'very sunny and warm today',
            "icon": 'd45'
        }
    ]
  
  def parse_daily_weather(self):
    payload = [
        {
            "date": "2020-10-01",
            "sunrise": "2020-09-30 13:27:03 -0600",
            "sunset": "2020-09-30 13:27:03 -0600",
            "max_temp": 79.4,
            "min_temp": 59.4,
            "conditions": 'very sunny and warm today',
            "icon": 'd45'
        }
    ]
