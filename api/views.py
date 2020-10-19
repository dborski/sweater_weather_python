import json
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView

from api.services.location_service import get_latlng
from api.services.weather_service import get_forecast
from api.services.photo_service import get_single_photo_by_keyword
from api.popos.forecast_parser import ForecastParser
from api.popos.photo_parser import PhotoParser


class ForecastView(APIView):
  def get(self, request):
    error_payload = {
        'success': False,
        'error': 400,
        'errors': "Must supply city and state ex. /forecast?location=denver,co"
    }

    location = request.GET['location']

    if location:
      split_location = location.split(",")
    else:
      return JsonResponse(error_payload, status=400)

    if len(split_location) == 2:
      results = get_latlng(split_location[0], split_location[1])
      forecast = get_forecast(str(results['lat']), str(results['lng'])).json()
      forecast_payload = ForecastParser(forecast).get_forecast_payload()
      return JsonResponse(forecast_payload)
    else:
      return JsonResponse(error_payload, status=400)
  

class BackgroundView(APIView):
  def get(self, request):
    error_payload = {
          'success': False,
          'error': 400,
          'errors': "Must search query param /backgrounds?location=denver,co"
    }

    if request.GET:
      location = request.GET['location']
      city = location.split(",")[0]
      photo_data = get_single_photo_by_keyword(city)
      background_payload = PhotoParser(photo_data, location).get_photo_payload()
      return JsonResponse(background_payload)
    else:
      return JsonResponse(error_payload, status=400)
