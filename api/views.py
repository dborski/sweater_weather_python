import json
from django.http import JsonResponse, QueryDict
from django.http import HttpResponse
from rest_framework.views import APIView

from api.services.location_service import get_latlng
from api.services.weather_service import get_forecast
from api.services.photo_service import get_single_photo_by_keyword
from api.popos.forecast_parser import ForecastParser
from api.popos.photo_parser import PhotoParser


class ForecastView(APIView):
  # parser_classes = [JSONParser]

  def get(self, request):
    # Capture location of requested city
    location = request.GET['location']

    # Split the location into city, state
    city, state = location.split(",")

    # get geocded lat and lng for the above locations
    results = get_latlng(city, state)

    # with lat and lng, get full forecast for city
    forecast = get_forecast(str(results['lat']), str(results['lng'])).json()

    forecast_payload = ForecastParser(forecast).get_forecast_payload()

    return JsonResponse(forecast_payload)

class BackgroundView(APIView):

  def get(self, request):
    location = request.GET['location']

    # split string and just use the city
    city = location.split(",")[0]

    # make api call to photo service with get single photo function
    photo_data = get_single_photo_by_keyword(city)

    # Grab information from api response and craft payload in PhotoParser
    background_payload = PhotoParser(photo_data, location).get_photo_payload()

    return JsonResponse(background_payload)
