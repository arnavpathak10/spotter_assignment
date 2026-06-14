from src.utils import utils
import math
from .services.station_finder import StationFinder
from .services.fuel_planner import FuelPlanner

util = utils()

class FuelOptimizer:
    def __init__(self):
        self.MAX_RANGE_MILES = 500
        self.MPG = 10     # miles per gallon
        self.station_finder = StationFinder()
        self.fuel_planner = FuelPlanner()


    def optimize(self, route_data): 

        distance_meters = route_data.get("distance_meters")

        duration_seconds = route_data.get("duration_seconds")

        distance_miles = util.meters_to_miles(distance_meters=distance_meters)

        duration_hrs = util.seconds_to_hours(duration_seconds=duration_seconds)

        fuel_needed = distance_miles / self.MPG

        required_stops = max(0, math.ceil(distance_miles / self.MAX_RANGE_MILES) -1)

        route_points = route_data.get("route_coordinates", [])

        # nearby_stations = []
        # if required_stops > 0:
        #     nearby_stations = self.station_finder.get_station_near_route(
        #         route_points=route_points, 
        #         routes_miles=5
        #     )

        fuel_stops = self.fuel_planner.plan(
            route_points=route_points, 
            required_stops=required_stops
            )
        
        avg_price = sum(stop["price"] for stop in fuel_stops) / len(fuel_stops) if fuel_stops else 3.0
        total_cost = fuel_needed * float(avg_price)


        return {
            # "recommended_stations": nearby_stations[:required_stops],
            "total_distance_miles" : round(distance_miles, 2),
            "total_duration_hours" : round(duration_hrs, 2),
            "fuel_needed" : round(fuel_needed, 2),
            "required_stops": int(required_stops),
            "total_cost" : round(total_cost, 2),
            "fuel_stops" : fuel_stops
        }