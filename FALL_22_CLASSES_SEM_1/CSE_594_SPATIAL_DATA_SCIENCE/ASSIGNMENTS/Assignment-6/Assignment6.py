from geotorch.datasets.grid import Processed
from torch.utils.data import DataLoader
from pyspark.sql import SparkSession
from sedona.register import SedonaRegistrator
from sedona.utils import SedonaKryoRegistrator, KryoSerializer
from geotorch.preprocessing import SparkRegistration, load_geo_data, load_data, load_geotiff_image, write_geotiff_image
from geotorch.preprocessing.enums import GeoFileType
from geotorch.preprocessing.enums import AggregationType
from geotorch.preprocessing.enums import GeoRelationship
from geotorch.preprocessing.raster import RasterProcessing as rp
from geotorch.preprocessing.grid import SpacePartition
from geotorch.preprocessing.grid import STManager as stm
from geotorch.preprocessing import Adapter
from geotorch.datasets.grid import Processed
from torch.utils.data import DataLoader
import itertools
import numpy as np


## create the st_tensor and write it to output_path
def create_st_tensor(path_to_shape_file, path_to_csv_file, output_path):
    print('Creating the tensor...')

    spark = SparkSession.builder.master("local[*]").appName("Sedona App").config("spark.serializer",
                                                                                 KryoSerializer.getName).config(
        "spark.kryo.registrator", SedonaKryoRegistrator.getName).config("spark.jars.packages",
                                                                        "org.apache.sedona:sedona-python-adapter-3.0_2.12:1.2.0-incubating,org.datasyslab:geotools-wrapper:geotools-24.0").getOrCreate()
    SedonaRegistrator.registerAll(spark)
    sc = spark.sparkContext
    sc.setSystemProperty("sedona.global.charset", "utf8")
    SparkRegistration.set_spark_session(spark)

    # load zones
    loadZones = load_geo_data(path_to_shape_file, GeoFileType.SHAPE_FILE)
    loadZones.CRSTransform("epsg:2263", "epsg:4326")

    # create zones df
    zonesDF = Adapter.rdd_to_spatial_df(loadZones)

    # create Grid, Taxi DF
    gridDF = SpacePartition.generate_grid_cells(zonesDF, "geometry", 32, 32)
    taxiDF = load_data(path_to_csv_file, data_format="csv", header="true")

    # select particular coloumns required for execution
    taxiDF = taxiDF.select("Trip_Pickup_DateTime", "Start_Lon", "Start_Lat")

    # preprocess data
    taxiDF = stm.trim_on_datetime(taxiDF, target_column="Trip_Pickup_DateTime", upper_date="2009-01-30 23:59:59",
                                  lower_date="2009-01-02 00:00:00")
    taxiDF = stm.get_unix_timestamp(taxiDF, "Trip_Pickup_DateTime", new_column_alias="converted_unix_time")
    taxiDF = stm.add_temporal_steps(taxiDF, timestamp_column="converted_unix_time", step_duration=1800,
                                    temporal_steps_alias="timesteps_id")

    # Get temporal steps
    total_temporal_setps = stm.get_temporal_steps_count(taxiDF, temporal_steps_column="timesteps_id")
    taxiDF = stm.add_spatial_points(taxiDF, lat_column="Start_Lat", lon_column="Start_Lon",

                                    new_column_alias="point_loc")

    # Create Col List
    column_list = ["point_loc"]
    agg_types_list = [AggregationType.COUNT]

    # Crate Alias List
    alias_list = ["point_cnt"]

    # apply agg functions on grid and taxiDF
    stDF = stm.aggregate_st_dfs(gridDF, taxiDF, "geometry", "point_loc", "cell_id", "timesteps_id",
                                GeoRelationship.CONTAINS, column_list, agg_types_list, alias_list)
    st_tensor = stm.get_st_grid_array(stDF, "timesteps_id", "cell_id", alias_list,
                                      temporal_length=total_temporal_setps, height=32, width=32, missing_data=0)
    st_tensor2 = np.swapaxes(st_tensor, 1, 3)
    st_tensor2 = np.swapaxes(st_tensor2, 2, 3)
    np.save(output_path, st_tensor2)


## returns the periodical representation of st_tensor

def load_tensor_periodical(path_to_tensor, len_closeness, len_period, len_trend, T_closeness, T_period, T_trend,
                           batch_size, batch_index):
    processed_obj = Processed(path_to_tensor, len_closeness=len_closeness, len_period=len_period, len_trend=len_trend,
                              T_closeness=T_closeness, T_period=T_period, T_trend=T_trend)
    train_dataloader = DataLoader(processed_obj, batch_size=batch_size)
    sample1 = next(iter(train_dataloader))
    return sample1["x_closeness"], sample1["x_period"], sample1["x_trend"], sample1["y_data"]


## returns the sequential representation of st_tensor

# Define Variables:
TEST_RATIO = 0.1
TRAINING_DATA = True

def load_tensor_sequential(path_to_tensor, len_history, len_predict, batch_size, batch_index):
    processedNext = Processed(path_to_tensor, is_training_data=TRAINING_DATA, test_ratio=TEST_RATIO)
    processedNext.merge_closeness_period_trend(history_length=len_history, predict_length=len_predict)
    trainDataLoader = DataLoader(processedNext, batch_size=batch_size)
    sample2 = next(iter(trainDataLoader))
    return sample2["x_data"], sample2["y_data"]
