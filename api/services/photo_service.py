import os
import requests
from dotenv import load_dotenv, find_dotenv
from django.http import JsonResponse
load_dotenv(find_dotenv())


class PhotoService:
    def get_photos_by_keyword(self, search_query):
        response = requests.get(
            'https://api.unsplash.com/search/photos',
            params={'query': f'{search_query}'},
            headers={'Authorization': f"{os.getenv('UNSPLASH_KEY')}"},
        )

        if response.status_code == 200:
            return response
        else:
            raise requests.RequestException

    def get_single_photo_by_keyword(self, search_query):
        results = self.get_photos_by_keyword(search_query)

        if results.status_code == 200:
            return results.json()['results'][0]
        else:
            raise requests.RequestException
