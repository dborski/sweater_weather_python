# Sweater Weather

Sweater Weather is the backend of a service-oriented application that builds and exposes multiple API endpoints. The application allows the user to plan road trips and see the current weather as well as the forecasted weather at the destination.

This was created by [Derek Borski](https://github.com/dborski)

API Services Used:
- OpenWeather
- MapQuest
- Unsplash

## API Endpoints

#### Forecast

```
GET /api/v1/forecast?location=<city>,<state>
```
Description:
- Displays the current, hourly, and daily forecast for the desired location
- Returns a 200 status code on success

```
{
    "data": {
        "id": null,
        "type": "forecast",
        "attributes": {
            "current_weather": {
                "datetime": "2020-10-26 12:13:15 -0753",
                "sunrise": "2020-10-26 06:58:01 -0753",
                "sunset": "2020-10-26 17:50:40 -0753",
                "temperature": 49.62,
                "feels_like": 30.24,
                "humidity": 11,
                "uvi": 3.72,
                "visibility": 10000,
                "conditions": "clear sky",
                "icon": "01d"
            },
            "daily_weather": [
                {
                    "date": "2020-10-26",
                    "sunrise": "2020-10-26 06:58:01 -0753",
                    "sunset": "2020-10-26 17:50:40 -0753",
                    "max_temp": 57.51,
                    "min_temp": 39.16,
                    "conditions": "clear sky",
                    "icon": "01d"
                },
                {
                    "date": "2020-10-27",
                    "sunrise": "2020-10-27 06:58:59 -0753",
                    "sunset": "2020-10-27 17:49:33 -0753",
                    "max_temp": 66.85,
                    "min_temp": 42.8,
                    "conditions": "clear sky",
                    "icon": "01d"
                },
                {...}
            ],
            "hourly_weather": [
                {
                    "time": "12:00:00",
                    "temp": 49.62,
                    "wind_speed": "21.63 mph",
                    "wind_direction": "from N",
                    "conditions": "clear sky",
                    "icon": "01d"
                },
                {
                    "time": "13:00:00",
                    "temp": 52.27,
                    "wind_speed": "20.96 mph",
                    "wind_direction": "from N",
                    "conditions": "clear sky",
                    "icon": "01d"
                },
                {...}
            ]
        }
    }
}
```

#### City Background

```
GET /api/v1/backgrounds?location=<city>,<state>
```
Description:
- Finds a relevant image for the city and state of the desired location
- Returns a 200 status code on success

Response Body:
```
{
    "data": {
        "type": "image",
        "id": null,
        "image": {
            "location": "denver,co",
            "image_url": "https://images.unsplash.com/photo-1546156929-a4c0ac411f47?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjE1MzI5N30",
            "credit": {
                "source": "unsplash.com",
                "author": "theadventurebitch",
                "logo": "https://unsplash-assets.imgix.net/marketing/press-logotype.svg?auto=format&fit=crop&q=60"
            }
        }
    }
}
```

#### User Registration

```
POST /api/v1/users
```
Description:
- Registers a new user for the site and generates a unique API key as credentials
- Returns a 201 status code on success

Required Request Body:
- JSON payload of:
  - email: Required, must be unique, cannot be blank
  - password: Required
  - password_confirmation: Required, must match password
```
{
    "email": "new_user6@email.com",
    "password": "password",
    "password_confirmation": "password"
}
```
Response Body:
```
{
    "data": {
        "type": "users",
        "id": 6,
        "attributes": {
            "email": "new_user6@email.com",
            "api_key": "bf97fdcb-b6f5-4dd2-89d2-3dd1cfcb742b"
        }
    }
}
```

#### User Login

```
POST /api/v1/sessions
```
Description:
- Logs a user into the site only if the user has the correct API key
- Returns a 201 status code on success

Required Request Body:
- JSON payload of:
  - username: Required
  - password: Required, must be correct password
```
{
    "username": "new_user6@email.com",
    "password": "password"
}

```
Response Body:
```
{
    "data": {
        "type": "users",
        "id": 5,
        "attributes": {
            "email": "new_user5@email.com",
            "api_key": "33c896e5-a625-41d5-bd2b-633670d6d817"
        }
    }
}
```

#### Create Road Trip

```
POST /api/v1/road_trip
```
Description:
- Calculates the travel time and weather upon arrival for a road trip and saves the road trip in the database for the user.
- Returns a 201 status code on success

Required Request Body:
- JSON payload of:
  - origin: Required
  - destination: Required
  - api_key: Required, must be correct api key for user
```
{
    "origin": "Denver,CO",
    "destination": "Las Vegas, NV",
    "api_key": "33c896e5-a625-41d5-bd2b-633670d6d817"
}
```
Response Body:
```
{
    "data": {
        "id": null,
        "type": "roadtrip",
        "attributes": {
            "start_city": "Denver,CO",
            "end_city": "Las Vegas, NV",
            "travel_time": "10 hours, 31 minutes",
            "weather_at_eta": {
                "temperature": 44.28,
                "conditions": "clear sky"
            }
        }
    }
}
```

