import pytz
from pytz import timezone
from datetime import datetime
import time

def _forecast_payload():
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


class ForecastParser:
    def __init__(self, forecast):
        self.timezone = forecast['timezone']
        self.timezone_offset = forecast['timezone_offset']
        self.current = forecast['current']
        self.hourly = forecast['hourly']
        self.daily = forecast['daily']
    
    def convert_to_formatted_string(self, number):
        return f'{number} mph'


    def convert_to_cardinals(self, degrees):
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

        ix = round(degrees / (360. / len(dirs)))
        cardinal = dirs[ix % len(dirs)]

        return f'from {cardinal}'

    def covert_to_localtime(self, utctime, new_format):
        format = '%Y-%m-%d %H:%M:%S %z'

        new_utc_time = utctime + self.timezone_offset
        local_time = time.strftime(format, time.localtime(new_utc_time))
        datetime_obj = datetime.strptime(local_time, format)
        datetime_new_tz = datetime_obj.replace(tzinfo=timezone(self.timezone))

        return datetime_new_tz.strftime(new_format)


    def parse_current_weather(self):
        format = '%Y-%m-%d %H:%M:%S %z'

        return {
                "datetime": self.covert_to_localtime(self.current['dt'], format),
                "sunrise": self.covert_to_localtime(self.current['sunrise'], format),
                "sunset": self.covert_to_localtime(self.current['sunset'], format),
                "temperature": self.current['temp'],
                "feels_like": self.current['feels_like'],
                "humidity": self.current['humidity'],
                "uvi": self.current['uvi'],
                "visibility": self.current['visibility'],
                "conditions": self.current['weather'][0]['description'],
                "icon": self.current['weather'][0]['icon']
        }

    def parse_hourly_weather(self):
        format = '%H:%M:%S'
        eight_hours = self.hourly[:8]
        hourly = []

        for weather_info in eight_hours:
            hourly.append(
                {
                    "time": self.covert_to_localtime(weather_info['dt'], format),
                    "temp": weather_info['temp'],
                    "wind_speed": self.convert_to_formatted_string(weather_info['wind_speed']),
                    "wind_direction": self.convert_to_cardinals(weather_info['wind_deg']),
                    "conditions": weather_info['weather'][0]['description'],
                    "icon": weather_info['weather'][0]['icon']
                }
            )

        return hourly

    def parse_daily_weather(self):
        date_format = '%Y-%m-%d'
        full_format = '%Y-%m-%d %H:%M:%S %z'
        five_days = self.daily[:5]
        daily = []

        for weather_info in five_days:
            daily.append(
                {
                    "date": self.covert_to_localtime(weather_info['dt'], date_format),
                    "sunrise": self.covert_to_localtime(weather_info['sunrise'], full_format),
                    "sunset": self.covert_to_localtime(weather_info['sunset'], full_format),
                    "max_temp": weather_info['temp']['max'],
                    "min_temp": weather_info['temp']['min'],
                    "conditions": weather_info['weather'][0]['description'],
                    "icon": weather_info['weather'][0]['icon']
                }
            )

        return daily

    def get_forecast_payload(self):
        payload = _forecast_payload().copy()
        payload['data']['attributes']['current_weather'] = self.parse_current_weather()
        payload['data']['attributes']['hourly_weather'] = self.parse_hourly_weather()
        payload['data']['attributes']['daily_weather'] = self.parse_daily_weather()

        return payload
