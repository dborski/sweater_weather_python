import json
from django.http import JsonResponse, QueryDict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from api.services.location_service import get_latlng
from api.services.weather_service import get_forecast


class ForecastView(APIView):
  parser_classes = [JSONParser]

  def get(self, request):
    # Capture location of requested city
    location = request.GET['location']

    # Split the location into city, state
    city, state = location.split(",")

    # get geocded lat and lng for the above locations
    results = get_latlng(city, state)

    # with lat and lng, get full forecast for city
    forecast = get_forecast(results['lat'], results['lng']).json()

    # Parse through full forecast to pull out only needed attributes
    # ForecastParser(forecast).forecast_payload
    # Setup forecast payload with blank hash to be filled in
    # Each part of the hash is filled in by the parser to complete payload

    # import code; code.interact(local=dict(globals(), **locals()))

    # return forecast_payload

    return ""
