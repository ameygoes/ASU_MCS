import geopandas as gpd
import numpy as np
import pandas as pd

EPSG_COORD = "EPSG:4326"


def find_hotspot(taxi_zones: gpd.GeoDataFrame, taxi_pickups: pd.DataFrame, output_path):
    txZoneDF = taxi_zones.to_crs(EPSG_COORD)

    pickUpLocs = gpd.GeoSeries.from_xy(taxi_pickups['pickup_longitude'], taxi_pickups['pickup_latitude'],
                                       crs=EPSG_COORD)

    txPickUpLocsDF = gpd.GeoDataFrame(geometry=pickUpLocs, crs=EPSG_COORD)

    df = gpd.sjoin(txZoneDF, txPickUpLocsDF, how='left', predicate='contains') \
        .groupby('LocationID') \
        .agg(freq=('index_right', 'count'), sq_freq=('index_right', lambda x: len(x) ** 2))

    Count = np.double(txZoneDF['LocationID'].count())

    valueOfX, Frequency, SquareOfX = CalculateXValues(df, Count)

    S = np.sqrt(Frequency - SquareOfX)

    Wij_df = gpd.sjoin(txZoneDF, txZoneDF, predicate='intersects') \
        .loc[lambda l: l["LocationID_left"] != l["LocationID_right"]] \
        .merge(df, how='left', left_on='LocationID_right', right_on='LocationID') \
        .rename(columns={'LocationID_left': 'LocationID'}) \
        .groupby('LocationID').agg(wijxj=('freq', 'sum'), wij=('LocationID_right', 'count'))

    Wij_df[' g_score'] = Wij_df.apply(lambda d: CalculateGScore(d['wijxj'], d['wij'], valueOfX, S, Count), axis=1)
    result = Wij_df.nlargest(50, ' g_score').drop(columns=['wijxj', 'wij']).reset_index(inplace=False)

    result.to_string(output_path, header=True, index=False)


def CalculateGScore(wijxj, wij, xbar, S, N):
    a = wijxj - (xbar * wij)
    b = S * np.sqrt((N * wij - wij * wij) / (N - 1.0))

    if b == 0.0:
        b = pow(10, -10)
    return a / b


def CalculateXValues(df, Cnt):
    valueOfX = np.double(df['freq'].sum()) / Cnt
    Frequency = np.double(df['sq_freq'].sum()) / Cnt
    SquareOfX = np.power(valueOfX, 2)
    return valueOfX, Frequency, SquareOfX
