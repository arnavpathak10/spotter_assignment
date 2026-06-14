import os 
import requests
from rest_framework.response import Response

class GeocodingServices:
    def __init__(self):
        self.api_key = os.getenv("ORS_API_KEY")

    def get_geocode(self, location):

        url = "https://api.openrouteservice.org/geocode/search"

        params = {
            "api_key": self.api_key,
            "text": location,
            "size": 1
        }

        response = requests.get(url, params=params)

        data = response.json()

        features = data.get("features", [])

        if not features:
            raise Exception(f"Location not found: {location}")

        longitude, latitude = features[0]["geometry"]["coordinates"]

        return [longitude, latitude]

