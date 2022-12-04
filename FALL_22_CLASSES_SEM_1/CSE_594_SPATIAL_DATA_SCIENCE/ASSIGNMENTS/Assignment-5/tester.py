
import geopandas as gpd
import pandas as pd
import numpy as np
import math
import Assignment5

## input and output paths
zones_path = "data/taxi-zones"
pickup_path = "data/yellow_tripdata_part.csv"
output_path = "output/g_scoresTest.txt"

if __name__ == '__main__':
	## loading the taxi zones shape file
	taxi_zones = gpd.read_file(zones_path)
	taxi_zones = taxi_zones[["LocationID", "geometry"]]

	## loading the csv containing taxi pickup locations
	taxi_pickups = pd.read_csv(pickup_path)
	taxi_pickups = taxi_pickups[["pickup_longitude", "pickup_latitude"]]

	## find the hotspot taxi zones in terms of pickup counts
	Assignment5.find_hotspot(taxi_zones, taxi_pickups, output_path)
