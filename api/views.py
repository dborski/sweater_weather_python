import json
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
import uuid

from api.services.location_service import get_latlng, get_directions
from api.services.weather_service import get_forecast
from api.services.photo_service import get_single_photo_by_keyword
from api.popos.forecast_parser import ForecastParser
from api.popos.photo_parser import PhotoParser
from api.popos.road_trip_creator import RoadTripCreator


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
      pass
    
    if body['password'] == body['password_confirmation']:
      return True
    else:
      errors.append("The passwords do not match")
      return False

def _login_success(request, body, user):
  if 'username' and 'password' in body:
    found_user = authenticate(request, username=body['username'], password=body['password'])
    if found_user is not None:
      user.append(found_user)
      login(request, found_user)
      return True
    else:
      return False
  else:
    False

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

def _error_payload(error, code=400):
  return {
      'success': False,
      'error': code,
      'errors': error
  }

class ForecastView(APIView):
  def get(self, request):
    location = request.GET['location']

    if location:
      split_location = location.split(",")
    else:
      return JsonResponse(_error_payload, status=400)

    if len(split_location) == 2:
      results = get_latlng(split_location[0], split_location[1])
      forecast = get_forecast(str(results['lat']), str(results['lng'])).json()
      forecast_payload = ForecastParser(forecast).get_forecast_payload()
      return JsonResponse(forecast_payload)
    else:
      error = "Must include city and state ex. /forecast?location=denver,co"
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
      error = "Must include search query param /backgrounds?location=denver,co"
      return JsonResponse(_error_payload(error), status=400)

class UserRegistrationView(APIView):
  def post(self, request):
    body = request.data
    errors = []

    if _registration_success(body, errors):
      new_user = User.objects.create_user(
        body['email'], 
        body['email'], 
        body['password']
      )
      return JsonResponse(_user_payload(new_user), status=201)
    else:
      return JsonResponse(_error_payload(errors[0]), status=400)

class UserLoginView(APIView):
  def post(self, request):
    body = request.data
    user = []

    if _login_success(request, body, user):
      return JsonResponse(_user_payload(user[0]), status=200)
    else:
      error = 'Credentials are incorrect'
      return JsonResponse(_error_payload(error, 401), status=401)

class RoadTripView(APIView):
  def post(self, request):
    body = request.data
    errors = []
    user = []

    if _road_trip_requirements_met(body, errors, user):
      trip_payload = RoadTripCreator(body['origin'], body['destination'], user[0]).create_road_trip()
      return JsonResponse(trip_payload, status=201)
    else:
      return JsonResponse(_error_payload(errors[0]))

def _road_trip_requirements_met(body, errors, user):
    if 'api_key' in body:
      pass
    else:
      errors.append("Must include API key")
      return False
    if 'origin' in body:
      pass
    else:
      errors.append("Must include origin")
      return False
    if 'destination' in body:
      pass
    else:
      errors.append("Must include destination")
      return False

    try:
      user.append(User.objects.get(profile__api_key=body['api_key']))
      return True
    except ObjectDoesNotExist:
      errors.append("This email already exists")
      return False