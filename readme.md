# Fuel Route Optimization API

## Overview

This project is a Django REST API that calculates an optimal fuel plan for a trip between two locations in the United States.

Given a start location and destination, the API:

- Calculates the driving route
- Determines how many fuel stops are required
- Finds fuel stations near the route
- Selects cost-effective stations based on fuel prices
- Estimates total fuel consumption
- Calculates total fuel cost for the trip

The application uses OpenRouteService for geocoding and route generation.

---

## Assumptions

- Vehicle fuel economy: 10 miles per gallon
- Maximum vehicle range on a full tank: 500 miles
- Fuel stop planning uses a small safety buffer before the maximum range is reached
- Fuel prices are loaded from the provided fuel price dataset

---

## Technologies Used

- Python 3
- Django
- Django REST Framework
- OpenRouteService API
- PostgreSQL

---

## API Endpoint

### Optimize Route

--POST--

```http
/api/optimize-route/
```

### Request Body

```json
{
    "start": "Dallas, TX",
    "destination": "Los Angeles, CA"
}
```

### Example Response

```json
{
    "total_distance_miles": 1442.67,
    "total_duration_hours": 22.05,
    "fuel_needed": 144.27,
    "required_stops": 2,
    "total_cost": 513.81,
    "fuel_stops": [
        {
            "id": 95,
            "name": "LOVES TRAVEL STOPS #256",
            "lat": 31.040253,
            "lon": -104.831363,
            "price": 3.649
        },
        {
            "id": 20,
            "name": "PETRO STOPPING CENTER #306",
            "lat": 32.778688,
            "lon": -111.596545,
            "price": 3.474
        }
    ]
}
```

---

## Project Flow

1. User submits a start and destination location.
2. The locations are geocoded into coordinates.
3. OpenRouteService generates the driving route.
4. Route distance and duration are calculated.
5. The application determines how many fuel stops are required based on the vehicle's maximum range.
6. Fuel stations near the route are identified.
7. The most cost-effective stations are selected using available fuel price data.
8. Total fuel consumption and trip fuel cost are calculated.
9. Results are returned as a JSON response.

---

## Installation

### Extract the project

```bash
cd fuel_optimizer
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
ORS_API_KEY=your_openrouteservice_api_key (I shared with my api key which is not good for production)
```

### Database Configuration

Update the database settings in your `.env` file:

- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_HOST
- DATABASE_PORT


### Run migrations

```bash
python manage.py migrate
```

### Load Fuel Price Data (IMPORTANT)

```bash
python manage.py import_fuel_prices
```

Import the provided fuel station and fuel price dataset into the database before running the API.

The imported data is used by the fuel optimization logic to determine cost-effective fuel stops.

### Populate Station Coordinates (IMPORTANT)

Run the management command below to geocode fuel stations and store latitude and longitude values in the database:

```bash
python manage.py geocode_stations
```

### Start the server

```bash
python manage.py runserver
```

---

## Notes

- The application makes a single routing request per API call.
- Fuel station locations are stored locally in the database.
- Fuel prices are loaded from the provided dataset.
- Fuel stop recommendations are selected based on route position and fuel price.
- The API is designed to return results quickly while minimizing external API calls.

---

## Submission

This project was developed as part of the Fuel Route Optimization assessment using Django and Django REST Framework.

## Author

Name: Arnav Kumar Pathak
email: arnavpathak.in@gmail.com
