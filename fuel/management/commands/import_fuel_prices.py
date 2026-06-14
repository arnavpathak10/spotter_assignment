import pandas as pd
from fuel.models import FuelStation, FuelPrice


def insert_fuel_prices_data(df):
    df = df.drop_duplicates()

    station_df = df.drop_duplicates(subset=["OPIS Truckstop ID"])

    stations = []

    for index, row in station_df.iterrows():
    
        stations.append(
            FuelStation(
            opis_truckstop_id = row["OPIS Truckstop ID"], 
            truckstop_name = row["Truckstop Name"],  
            address = row["Address"],  
            city = row["City"], 
            state = row["State"]
            )
        )
        
    FuelStation.objects.bulk_create(stations, ignore_conflicts=True)
    

    station_lookup = {station.opis_truckstop_id : station for station in FuelStation.objects.all()}


    prices = []

    for index, row in df.iterrows():

        station = station_lookup[row["OPIS Truckstop ID"]]

        prices.append(
            FuelPrice(
                station = station, 
                rack_id = row["Rack ID"], 
                retail_price = row["Retail Price"]
                )
            )
        
    FuelPrice.objects.bulk_create(prices, ignore_conflicts=True)
    

df = pd.read_csv("data/fuel-prices-for-be-assessment.csv")

if not FuelStation.objects.all().exists():
    insert_fuel_prices_data(df=df)

