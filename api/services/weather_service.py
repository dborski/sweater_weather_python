import os
import requests
from dotenv import load_dotenv, find_dotenv
from django.http import JsonResponse
load_dotenv(find_dotenv())


class WeatherService:
    def get_forecast(self, lat, lng, exclude='minutely', units='imperial'):
        response = requests.get(
            'https://api.openweathermap.org'
            '/data/2.5/onecall'
            f"?appid={os.getenv('OPENWEATHER_KEY')}"
            f'&lat={lat}'
            f'&lon={lng}'
            f'&exclude={exclude}'
            f'&units={units}'
        )

        if response.status_code == 200:
            return response
        else:
            raise requests.RequestException
