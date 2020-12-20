from .base_view import *
from api.services.photo_service import PhotoService
from api.popos.forecast_parser import ForecastParser
from api.popos.photo_parser import PhotoParser


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
            error = 'Must include city and state ex. /forecast?location=denver,co'
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
            error = 'Must include search query param /backgrounds?location=denver,co'
            return JsonResponse(error_payload(error), status=400)
