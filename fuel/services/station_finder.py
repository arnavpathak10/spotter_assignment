from fuel.models import FuelStation, FuelPrice
from src.utils import utils 


class StationFinder:
    def __init__(self):
        self.util = utils()

    def get_station_near_route(self, route_points, routes_miles = 5):
        stations = FuelStation.objects.filter(latitude__isnull=False, longitude__isnull=False)

        nearby_stations = []
        seen = set()

        for station in stations:

            for point in route_points:

                lon, lat = point

                route_distance_miles = self.util.haversine(
                    station_lat=station.latitude,
                    station_lon=station.longitude, 
                    route_lat=lat,
                    route_lon=lon
                    )

                if route_distance_miles <= routes_miles: 
                    if station.id not in seen: 
                        nearby_stations.append(
                            {
                                "id": station.id,
                                "name": station.truckstop_name,
                                "lat": station.latitude,
                                "lon": station.longitude,
                                "price" : FuelPrice.objects.filter(
                                    station=station.id).order_by(
                                        "retail_price").first().retail_price
                            }
                        )
                        seen.add(station.id)
                    break

        return nearby_stations


