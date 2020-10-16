import os
import json
import requests
from dotenv import load_dotenv, find_dotenv
from django.http import JsonResponse
load_dotenv(find_dotenv())

def get_latlng(city, state):
    payload = {
      'lat': float,
      'lng': float,
    }

    response = requests.get(
        'http://www.mapquestapi.com'
        '/geocoding/v1/address'
        f"?key={os.getenv('MAPQUEST_KEY')}"
        f'&location={city},{state}'
    )
    
    if response.status_code == 200:
      latlng = response.json()['results'][0]['locations'][0]['latLng']
      payload['lat'] = latlng['lat']
      payload['lng'] = latlng['lng']
      return payload
    else:
      raise requests.RequestException
