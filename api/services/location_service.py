import os
import requests
from dotenv import load_dotenv, find_dotenv
from django.http import JsonResponse
load_dotenv(find_dotenv())


class LocationService:
    def get_latlng(self, city, state):
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
    
    def get_directions(self, start_location, end_location):
        from_city, from_state = start_location.lower().split(",")
        to_city, to_state = end_location.lower().split(",")

        response = requests.get(
            'http://www.mapquestapi.com'
            '/directions/v2/route'
            f"?key={os.getenv('MAPQUEST_KEY')}"
            f'&from={from_city},{from_state}'
            f'&to={to_city},{to_state}'
        )

        if response.status_code == 200:
            return response
        else:
            raise requests.RequestException