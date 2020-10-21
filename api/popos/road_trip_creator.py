from datetime import datetime
from api.models import RoadTrip
from api.services.location_service import get_directions, get_latlng
from api.services.weather_service import get_forecast



def _road_trip_payload(road_trip):
  return {
      "data": {
          "id": None,
          "type": "roadtrip",
          "attributes": {
              "start_city": road_trip.start_city,
              "end_city": road_trip.end_city,
              "travel_time": road_trip.travel_time,
              "weather_at_eta": {
                  'temperature': road_trip.arrival_temp,
                  'conditions': road_trip.arrival_conditions
              }
          }
      }
  }

def _error_payload(start_location, end_location):
  return {
      "data": {
          "id": None,
          "type": "roadtrip",
          "attributes": {
              "start_city": start_location,
              "end_city": end_location,
              "travel_time": 'Impossible',
              "weather_at_eta": None
          }
      }
  }

class RoadTripCreator:
  def __init__(self, start_location, end_location, user):
    self.start_location = start_location
    self.end_location = end_location
    self.directions = get_directions(start_location, end_location).json()
    self.user = user

  def get_travel_time(self):
    if self.directions['route']['routeError']['errorCode'] == 2:
      return 'Impossible'
    else:
      travel_time = self.directions['route']['formattedTime']
      travel_object = datetime.strptime(travel_time, '%y:%M:%S')

      if travel_object.year == 0:
        new_string = travel_object.strftime('%-M minutes')
      else:
        new_string = travel_object.strftime('%y hours, %-M minutes')

      return new_string, travel_object
  
  def get_weather_at_eta(self):
    payload = {
      'temperature': None,
      'conditions': None
    }
    # Get travel time in hours and minutes
    travel_time = self.get_travel_time()
    
    if travel_time == 'Impossible':
      return None
    else:
      # Get lat and lng for end location
      travel_time = travel_time[1]
      city, state = self.end_location.split(',')
      latlng = get_latlng(city, state)

      # Get weather for end location, specifically hourly
      forecast = get_forecast(latlng['lat'], latlng['lng']).json()

      # Find total travel time in travel_time variable
      hours = travel_time.hour
      minutes = (travel_time.minute / 60)
      rounded = round(hours + minutes)

      # Add travel time hours to hourly weather forecast
      # Pull temperature and conditions from specified hourly forecast
      destination_forecast = forecast['hourly'][rounded]

      # add data to payload
      payload['temperature'] = destination_forecast['temp']
      payload['conditions'] = destination_forecast['weather'][0]['description'] 

      return payload

  def name_creator(self):
    return f'Road trip from {self.start_location} to {self.end_location}'

  def create_road_trip(self):
    travel_time = self.get_travel_time()
    weather = self.get_weather_at_eta()

    if travel_time != 'Impossible':
      new_trip = RoadTrip.objects.create(
        user=self.user,
        name=self.name_creator(),
        start_city=self.start_location,
        end_city=self.end_location,
        travel_time=travel_time[0],
        arrival_temp=weather['temperature'],
        arrival_conditions=weather['conditions']
      )
      return _road_trip_payload(new_trip)
    else:
      return _error_payload(self.start_location, self.end_location)
    

