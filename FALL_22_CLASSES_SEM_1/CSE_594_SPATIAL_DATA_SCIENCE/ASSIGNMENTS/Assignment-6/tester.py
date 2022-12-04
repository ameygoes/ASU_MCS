
import numpy as np
import Assignment6

## input and output paths
zones_path = "data/taxi_trip/taxi_zones"
pickup_path = "data/taxi_trip/yellow_tripdata_2009-01.csv"
output_path = "output/st_tensor.npy"

if __name__ == '__main__':

	Assignment6.create_st_tensor(zones_path, pickup_path, output_path)

	x_closeness, x_period, x_trend, y_data = Assignment6.load_tensor_periodical(path_to_tensor=output_path, len_closeness=2, len_period=3, len_trend=3, T_closeness=1, T_period=12, T_trend=12*7, batch_size=4, batch_index=0)
	print(x_closeness.shape, x_period.shape, x_trend.shape, y_data.shape)

	x_data, y_data = Assignment6.load_tensor_sequential(path_to_tensor=output_path, len_history=22, len_predict=2, batch_size=4, batch_index=0)
	print(x_data.shape, y_data.shape)
	
