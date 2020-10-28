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
api/v1/forecast?location=<city>,<state>
```

Displays the current, hourly, and daily forecast for the desired location

#### City Background

```
api/v1/backgrounds?location=<city>,<state>
```

Finds a relevant image for the city and state of the desired location

#### User Registration

```
api/v1/users
```

Registers a new user for the site and generates a unique API key as credentials

#### User Login

```
api/v1/sessions
```

Logs a user into the site only if the user has the correct API key

#### Create Road Trip

```
api/v1/road_trip
```

Calculates the travel time and weather upon arrival for a road trip and saves the road trip in the database for the user.

