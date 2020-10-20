from api.services.location_service import get_directions

def _road_trip_payload(road_trip):
  return {
      "data": {
          "id": None,
          "type": "roadtrip",
          "attributes": {
              "start_city": None,
              "end_city": None,
              "travel_time": None,
              "weather_at_eta": {
                  "temperature": None,
                  "conditions": None
              }
          }
      }
  }

class RoadTripCreator:
  def __init__(self, start_location, end_location, user):
    self.start_location = start_location
    self.end_location = end_location
    self.directions = get_directions(start_location, end_location)
    self.user = user

  # def get_travel_time(self):
  #   ''
  
  # def get_weather_at_eta(self):
  #   ''

  # def create_road_trip(self):
  #   ''
  
  # def get_road_trip_payload(self):
  #   ''
