import os
import requests
from src.geocoding_service import GeocodingServices
from rest_framework.response import Response


class RouteService:
    def __init__(self):
        self.api_key = os.getenv("ORS_API_KEY")
        self.geocoder = GeocodingServices()

    def get_route(self, start, destination):
        
        url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

        payload = {
            "coordinates" : [
                self.geocoder.get_geocode(start), 
                self.geocoder.get_geocode(destination)
            ]
        }

        headers = {
            "Authorization" : self.api_key,
            "content-type"  : "application/json"
            }
        

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        # print(data, "printing data from route_service python")


        if "features" not in data:
            raise Exception(data)

        feature = data["features"][0]

        properties = feature["properties"]

        distance = properties["summary"]["distance"]
        duration = properties["summary"]["duration"]

        coordinates = feature["geometry"]["coordinates"]

        segments = properties["segments"]
        steps = segments[0]["steps"]


        return {
            "distance_meters": distance,
            "duration_seconds": duration,
            "route_coordinates": coordinates,
            "steps": steps,
        }

