import json
from django.http import JsonResponse, QueryDict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

class ForecastView(APIView):
  parser_classes = [JSONParser]

  def get(self, request):
    # Capture location of requested city
    location = request.GET['location']

    # Split the location into state, city

    # get geocded lat and lng for the above locations

    # with lat and lng, get full forecast for city

    # Parse through full forecast to pull out only needed attributes

    # Setup forecast payload with blank hash to be filled in

    # Each part of the hash is filled in by the parser to complete payload
    return "Hello"
