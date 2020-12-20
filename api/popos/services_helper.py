from api.services.location_service import LocationService
from api.services.photo_service import PhotoService
from api.services.weather_service import WeatherService

def get_geocoded_weather(city, state):
    results = LocationService().get_latlng(city, state)

    return WeatherService().get_forecast(str(results['lat']), str(results['lng']))