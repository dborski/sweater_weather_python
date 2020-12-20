from .base_view import *

from api.services.photo_service import PhotoService
from api.popos.forecast_parser import ForecastParser
from api.popos.photo_parser import PhotoParser
from api.popos.road_trip_creator import RoadTripCreator


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
        pass
    else:
        success = True
    
    return success, errors, user

class ForecastView(APIView):
    def get(self, request):
        location = request.GET['location']

        if location:
            split_location = location.split(",")
        else:
            error = 'Missing location query parameter'
            return JsonResponse(error_payload(error), status=400)

        if len(split_location) == 2:
            forecast = sh.get_geocoded_weather(split_location[0], split_location[1]).json()
            forecast_payload = ForecastParser(forecast).get_forecast_payload()

            return JsonResponse(forecast_payload)
        else:
            error = "Must include city and state ex. /forecast?location=denver,co"
            return JsonResponse(error_payload(error), status=400)
  
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
            return JsonResponse(error_payload(error), status=400)

class RoadTripView(APIView):
    def post(self, request):
        body = request.data
        success, errors, user = _road_trip_requirements_met(body)

        if success:
            return RoadTripCreator(body['origin'], body['destination'], user).create_road_trip()
        else:
            return JsonResponse(error_payload(','.join(errors)), status=400)
