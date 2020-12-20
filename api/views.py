from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
import uuid

import api.popos.services_helper as sh
from api.services.photo_service import PhotoService
from api.popos.forecast_parser import ForecastParser
from api.popos.photo_parser import PhotoParser
from api.popos.road_trip_creator import RoadTripCreator


def _registration_success(body):
    requirements = ['email', 'password', 'password_confirmation']
    body_params = set(body)
    success = False

    # check if there are any fields missing
    errors = [f'Missing {req}' for req in requirements if req not in body_params]

    if errors:
        return success, errors

    # check if email is unique
    try:
        user = User.objects.get(email=body['email'])
    except ObjectDoesNotExist:
        pass
    else:
        errors.append("This email already exists")
        return success, errors

    # check if passwords match
    if body['password'] == body['password_confirmation']:
        success = True
    else:
        errors.append("The passwords do not match")

    return success, errors


def _road_trip_requirements_met(body):
    requirements = ['api_key', 'origin', 'destination']
    body_params = set(body)
    user = None
    success = False

    # check if there are any fields missing
    errors = [f'Must include {req}' for req in requirements if req not in body_params]

    if errors:
        return success, errors, user

    # check if a user with submitted API key exists
    try:
        user = User.objects.get(profile__api_key=body['api_key'])
    except ObjectDoesNotExist:
        errors.append('A user does not exist with this API key')
    else:
        success = True
    
    return success, errors, user

def _login_success(request, body):
    requirements = ['username', 'password']
    body_params = set(body)
    user = None

    # check if there are any fields missing
    errors = [f'Must include {req}' for req in requirements if req not in body_params]

    if not errors:
        user = authenticate(request, username=body['username'], password=body['password'])
        if user is not None:
            login(request, user)
            success = True
        else:
            errors.append('Credentials are invalid')
            success =  False
    else:
        success = False

    return success, errors, user

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
            error = 'Missing location query parameter'
            return JsonResponse(_error_payload(error), status=400)

        if len(split_location) == 2:
            forecast = sh.get_geocoded_weather(split_location[0], split_location[1]).json()
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
            photo_data = PhotoService().get_single_photo_by_keyword(city)
            background_payload = PhotoParser(photo_data, location).get_photo_payload()
            return JsonResponse(background_payload)
        else:
            error = "Must include search query param /backgrounds?location=denver,co"
            return JsonResponse(_error_payload(error), status=400)

class UserRegistrationView(APIView):
    def post(self, request):
        body = request.data
        success, errors = _registration_success(body)

        if success:
            new_user = User.objects.create_user(
                body['email'], 
                body['email'], 
                body['password']
            )
            return JsonResponse(_user_payload(new_user), status=201)
        else:
            return JsonResponse(_error_payload(','.join(errors)), status=400)

class UserLoginView(APIView):
    def post(self, request):
        body = request.data
        success, errors, user = _login_success(request, body)

        if success:
            return JsonResponse(_user_payload(user), status=200)
        else:
            return JsonResponse(_error_payload('.'.join(errors), 401), status=401)

class RoadTripView(APIView):
    def post(self, request):
        body = request.data
        success, errors, user = _road_trip_requirements_met(body)

        if success:
            return RoadTripCreator(body['origin'], body['destination'], user).create_road_trip()
        else:
            return JsonResponse(_error_payload(','.join(errors)), status=400)
