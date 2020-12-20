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

    # check if there are any fields missing
    errors = [f'Missing {req}' for req in requirements if req not in body_params]

    if errors:
        return False, errors

    # check if email is unique
    try:
        user = User.objects.get(email=body['email'])
    except ObjectDoesNotExist:
        pass
    else:
        errors.append("This email already exists")
        return False, errors

    # check if passwords match
    if body['password'] == body['password_confirmation']:
        return True, '_'
    else:
        errors.append("The passwords do not match")
        return False, errors


def _road_trip_requirements_met(body, user):
    requirements = ['api_key', 'origin', 'destination']
    body_params = set(body)

    # check if there are any fields missing
    errors = [f'Must include {req}' for req in requirements if req not in body_params]

    if errors:
        return False, errors

    # check if a user with submitted API key exists
    try:
        user.append(User.objects.get(profile__api_key=body['api_key']))
    except ObjectDoesNotExist:
        return False, 'A user does not exist with this API key'
    else:
        return True, '_'

def _login_success(request, body, user):
    requirements = ['username', 'password']
    body_params = set(body)

    # check if there are any fields missing
    errors = [f'Must include {req}' for req in requirements if req not in body_params]

    if not errors:
        found_user = authenticate(request, username=body['username'], password=body['password'])
        if found_user is not None:
            user.append(found_user)
            login(request, found_user)
            return True, '_'
        else:
            errors.append('Credentials are invalid')
            return False, errors
    else:
        return False, errors

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
        reg_results = _registration_success(body)

        if reg_results[0]:
            new_user = User.objects.create_user(
                body['email'], 
                body['email'], 
                body['password']
            )
            return JsonResponse(_user_payload(new_user), status=201)
        else:
            return JsonResponse(_error_payload(','.join(reg_results[1])), status=400)

class UserLoginView(APIView):
    def post(self, request):
        body = request.data
        user = []
        login_results = _login_success(request, body, user)

        if login_results[0]:
            return JsonResponse(_user_payload(user[0]), status=200)
        else:
            return JsonResponse(_error_payload('.'.join(login_results[1]), 401), status=401)

class RoadTripView(APIView):
    def post(self, request):
        body = request.data
        user = []
        requirements = _road_trip_requirements_met(body, user)

        if requirements[0]:
            return RoadTripCreator(body['origin'], body['destination'], user[0]).create_road_trip()
        else:
            return JsonResponse(_error_payload(','.join(requirements[1])), status=400)
