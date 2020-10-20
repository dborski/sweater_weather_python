from datetime import datetime
from api.services.location_service import get_directions, get_latlng
from api.services.weather_service import get_forecast



def _road_trip_payload(road_trip):
  return {
      "data": {
          "id": None,
          "type": "roadtrip",
          "attributes": {
              "start_city": None,
              "end_city": None,
              "travel_time": None,
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
      travel_object = datetime.strptime(travel_time, '%H:%M:%S')

      if travel_object.hour == 0:
        new_string = travel_object.strftime('%-M minutes')
      else:
        new_string = travel_object.strftime('%-H hours, %-M minutes')

      return new_string, travel_object
  
  def get_weather_at_eta(self):
    payload = {
      'temperature': None,
      'conditions': None
    }
    # Get travel time in hours and minutes
    travel_time = self.get_travel_time()
    
    if travel_time == 'Impossible':
      payload['temperature'] = 'Impossible'
      payload['conditions'] = 'Impossible'
      return payload
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
      added = hours + minutes
      rounded = round(added)

      # Add travel time hours to hourly weather forecast
      # Pull temperature and conditions from specified hourly forecast
      destination_forecast = forecast['hourly'][rounded + 1]

      # add data to payload
      payload['temperature'] = destination_forecast['temp']
      payload['conditions'] = destination_forecast['weather'][0]['description'] 

      return payload



  # def create_road_trip(self):
  #   ''
  
  # def get_road_trip_payload(self):
  #   ''
