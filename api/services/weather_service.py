import os
import json
import requests
from dotenv import load_dotenv, find_dotenv
from django.http import JsonResponse
load_dotenv(find_dotenv())

def get_forecast(lat, lng, exclude='minutely'):
    response = requests.get(
        'https://api.openweathermap.org'
        '/data/2.5/onecall'
        f"?appid={os.getenv('OPENWEATHER_KEY')}"
        f'&lat={lat}'
        f'&lon={lng}'
        f'&exclude={exclude}'
    )

    if response.status_code == 200:
      return response
    else:
      raise requests.RequestException
