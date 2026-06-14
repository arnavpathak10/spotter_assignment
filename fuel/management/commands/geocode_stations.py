from src.geocoding_service import GeocodingServices
from fuel.models import FuelStation


fuel_station = FuelStation.objects.filter(latitude__isnull=True, longitude__isnull=True)[:100]

service = GeocodingServices()

if fuel_station.exists():
    for station in fuel_station:
        full_address = (f"{station.address}, {station.city}, {station.state}, USA")

        try: 
            coordinates = service.get_geocode(full_address)
        except: 
            continue
        
        if not coordinates:
            full_address = (f"{station.truckstop_name}, {station.address}, {station.city}, {station.state}, USA")
        
            coordinates = service.get_geocode(full_address)
            
        if not coordinates:
            print(f"Failed: {station.truckstop_name}")
            continue

        station.latitude = coordinates[1]
        station.longitude = coordinates[0]
        station.save(update_fields=["latitude", "longitude"])






