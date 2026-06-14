from math import radians, sin, cos, atan2, sqrt

class utils:

    def meters_to_miles(self, distance_meters):
        return distance_meters / 1609.344
    
    def seconds_to_hours(self, duration_seconds):
        return duration_seconds / 3600
    
    def haversine(self, station_lat, station_lon, route_lat, route_lon):
        
        R = 3959  # miles

        dlat = radians(route_lat - station_lat)
        dlon = radians(route_lon - station_lon)

        a = (
            sin(dlat / 2) ** 2
            + cos(radians(station_lat))
            * cos(radians(route_lat))
            * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c