
def _forecast_payload(forecast):
  return {
      "data": {
          "id": None,
          "type": "forecast",
          "attributes": {
              "current_weather": {
                  "datetime": "2020-09-30 13:27:03 -0600",
                  "sunrise": "2020-09-30 13:27:03 -0600",
                  "sunset": "2020-09-30 13:27:03 -0600",
                  "temperature": 79.4,
                  "feels_like": 79.4,
                  "humidity": 30,
                  "uvi": 15,
                  "visibility": 15,
                  "conditions": 'very sunny and warm today',
                  "icon": 'd45'
              },
              "daily_weather": [
                  {
                      "date": "2020-10-01",
                      "sunrise": "2020-09-30 13:27:03 -0600",
                      "sunset": "2020-09-30 13:27:03 -0600",
                      "max_temp": 79.4,
                      "min_temp": 59.4,
                      "conditions": 'very sunny and warm today',
                      "icon": 'd45'
                  }
              ],
              "hourly_weather": [
                  {
                      "time": "14:00:00",
                      "wind_speed": "4 mph",
                      "wind_direction": "from NW",
                      "conditions": 'very sunny and warm today',
                      "icon": 'd45'
                  }
              ]
          }
      }
  }

class ForecastParser:
  def __init__(self, forecast):
    self.timezone = forecast['timezone']
    self.timezone_offeset = forecast['timezone_offset']
    self.current = forecast['current']
    self.hourly = forecast['hourly']
    self.daily = forecast['daily']

