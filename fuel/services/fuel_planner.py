from .station_finder import StationFinder
from src.utils import utils
from fuel.models import FuelPrice


util = utils()

class FuelPlanner:
    def __init__(self):
        self.station_finder = StationFinder()
        self.MAX_RANGE_MILES = 500
        self.TOLERANCE = 20 


    def plan(self, route_points, required_stops=0):

        print(len(route_points), "print len route")


        if required_stops == 0:
            return []

        stops = []
        distance_accumulated = 0

        current_fuel_limit = self.MAX_RANGE_MILES - self.TOLERANCE

        price_map = {}
          
        
        for price in FuelPrice.objects.all().order_by("retail_price"):
            if price.station_id not in price_map:
                price_map[price.station_id] = price.retail_price


        for i in range(1, len(route_points)):

            lon1, lat1 = route_points[i - 1]
            lon2, lat2 = route_points[i]

            segment_distance = util.haversine(lat1, lon1, lat2, lon2)

            distance_accumulated += segment_distance


            if distance_accumulated >= current_fuel_limit:
                print("REFUEL POINT HIT", distance_accumulated)

                current_point = route_points[i]

                window_points = route_points[i - 200:i + 200]

                candidates = self.station_finder.get_station_near_route(
                    route_points=window_points,
                    routes_miles=5
                )
                print(candidates, "candidates from fuel planner route miles = 5")



                if not candidates:
                    candidates = self.station_finder.get_station_near_route(
                        route_points=window_points,
                        routes_miles=15
                    )
                    print(candidates, "candidates from fuel planner route miles = 15")
                


                if not candidates:
                    candidates = self.station_finder.get_station_near_route(
                        route_points=window_points,
                        routes_miles=25
                    )
                    print(candidates, "candidates from fuel planner route miles = 25")


                if not candidates:
                    candidates = self.station_finder.get_station_near_route(
                        route_points=window_points,
                        routes_miles=50
                    )
                    print(candidates, "candidates from fuel planner route miles = 50")
                    

                best_station = self.select_best_station(
                    candidates=candidates,
                    price_map=price_map
                )

                if best_station:
                    stops.append(best_station)

                distance_accumulated = 0

                if len(stops) == required_stops:
                    break

        return stops
    

    def select_best_station(self, candidates, price_map):
        if not candidates:
            return None
        
        best_station = None
        best_score = float("inf")

        for station in candidates:

            station_id = station["id"]

            price = price_map.get(station_id)

            if price is None:
                continue

            if price <= best_score:
                best_score = price


                best_station = {
                    "id": station["id"],
                    "name": getattr(station, "truckstop_name", station["name"]),
                    "lat" : station["lat"],
                    "lon": station["lon"],
                    "price": price
                }

        return best_station

            