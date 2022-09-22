#
# Assignment2
#

import geopandas as gpd

# Do not close the connection inside this file i.e. do not perform connection.close() or engine.close()


def load_shape_data(engine, input_path):
	## **TO DO**
	pass # remove it after finish the coding for this method




def explore_spatial_sql(connection, input_path, output_path1, output_path2, output_path3, output_path4, output_path5, output_path6, output_path7, output_path8):
	## **TO DO**
	pass # remove it after finish the coding for this method



def write_output(results, output_path):
	f = open(output_path, "w")
	for values in results:
		f.write(str(values[0]) + "\n")
	f.close()

	


