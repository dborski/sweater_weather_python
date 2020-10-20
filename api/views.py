import json
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import uuid

from api.services.location_service import get_latlng
from api.services.weather_service import get_forecast
from api.services.photo_service import get_single_photo_by_keyword
from api.popos.forecast_parser import ForecastParser
from api.popos.photo_parser import PhotoParser


def _registration_success(body, errors):
    if 'email' in body:
      pass
    else:
      errors.append("Missing email")
      return False
    
    if 'password' in body:
      pass
    else:
      errors.append("Missing password")
      return False

    if 'password_confirmation' in body:
      pass
    else:
      errors.append("Missing password confirmation")
      return False

    try:
      user_check = User.objects.get(email=body['email'])
      errors.append("This email already exists")
      return False
    except ObjectDoesNotExist:
      ''
    
    if body['password'] == body['password_confirmation']:
      return True
    else:
      errors.append("The passwords do not match")
      return False

def _user_payload(user):
  return {
      "data": {
          "type": "users",
          "id": user.id,
          "attributes": {
              "email": user.email,
              "api_key": user.profile.api_key
          }
      }
  }

def _error_payload(error):
  return {
      'success': False,
      'error': 400,
      'errors': error
  }

class ForecastView(APIView):
  def get(self, request):
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
      error = "Must supply city and state ex. /forecast?location=denver,co"
      return JsonResponse(_error_payload(error), status=400)
  

class BackgroundView(APIView):
  def get(self, request):
    if request.GET:
      location = request.GET['location']
      city = location.split(",")[0]
      photo_data = get_single_photo_by_keyword(city)
      background_payload = PhotoParser(photo_data, location).get_photo_payload()
      return JsonResponse(background_payload)
    else:
      error = "Must search query param /backgrounds?location=denver,co"
      return JsonResponse(_error_payload(error), status=400)

class UserRegistrationView(APIView):
  def post(self, request):
    body = request.data
    errors = []

    if _registration_success(body, errors):
      new_user = User.objects.create_user(body['email'], body['email'], body['password'])
      new_user.profile.api_key = str(uuid.uuid4())
      return JsonResponse(_user_payload(new_user), status=201)
    else:
      return JsonResponse(_error_payload(errors[0]), status=400)
