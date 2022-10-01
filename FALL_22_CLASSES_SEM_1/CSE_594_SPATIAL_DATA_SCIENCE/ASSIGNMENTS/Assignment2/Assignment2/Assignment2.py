import geopandas as gpd


def load_shape_data(engine, input_path):
    table_name = "shape_data"
    dfAirbnb = gpd.read_file(input_path)
    dfAirbnb.head()
    dfAirbnb.to_postgis(table_name, engine)


def explore_spatial_sql(connection, input_path, output_path3, output_path4, output_path5, output_path6, output_path7,
                        output_path8, output_path9, output_path10):
    # =============== DECLARATIONS =============
    cur = connection.cursor()
    SR_ID_VAL = 4326
    PT_TABLE_NAME = "point_data"
    SD_TABLE_NAME = "shape_data"
    POINT_DEF = "POINT(-87.60914087617012 41.84469250346108)"

    # DEFINE ALL QUERIES HERE
    TASK_2_QUERY = f"""CREATE TABLE {PT_TABLE_NAME}(latitude real, longitude real, geom geometry(Point,{SR_ID_VAL}) 
                   GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), {SR_ID_VAL}))
                   STORED);"""

    TASK_3_QUERY = f"""SELECT count(pd.geom) AS total_count FROM {PT_TABLE_NAME} pd, {SD_TABLE_NAME} sd 
                   WHERE ST_Within(pd.geom,sd.geometry) 
                   GROUP BY sd.community 
                   ORDER BY total_count ASC;"""

    TASK_4_QUERY = f"""SELECT count(sd2.geometry) AS total_count 
                   FROM {SD_TABLE_NAME} sd1, {SD_TABLE_NAME} sd2 
                   WHERE ST_Intersects(sd1.geometry,sd2.geometry) 
                   GROUP BY sd2.community 
                   ORDER BY total_count ASC"""

    TASK_5_QUERY = f"""SELECT ST_HausdorffDistance(ST_GeomFromText('{POINT_DEF}',4326), {SD_TABLE_NAME}.geometry) as hDist
                   FROM {SD_TABLE_NAME}
                   ORDER BY hDist ASC;"""

    TASK_6_QUERY = f"""SELECT ST_MaxDistance(ST_GeomFromText('{POINT_DEF}',4326), {SD_TABLE_NAME}.geometry) as maxDist
                   FROM {SD_TABLE_NAME}
                   ORDER BY maxDist ASC;"""

    TASK_7_QUERY = f"""SELECT ST_Perimeter(ST_ConvexHull({SD_TABLE_NAME}.geometry)) as boundary_length
                   FROM {SD_TABLE_NAME}
                   ORDER BY boundary_length"""

    TASK_8_QUERY = f"""SELECT ST_Area(geometry) as area
                   FROM {SD_TABLE_NAME}
                   WHERE ST_geometrytype(geometry)='ST_Polygon'
                   ORDER BY area ASC;"""

    TASK_9_QUERY = f"""SELECT ST_AsText(ST_ClosestPoint(ST_Envelope({SD_TABLE_NAME}.geometry), ST_GeomFromText('{POINT_DEF}',{SR_ID_VAL}))) as minDist
                   FROM shape_data
                   ORDER BY minDist ASC;"""

    TASK_10_QUERY = f"""SELECT ST_Area(ST_Intersection(ST_GeomFromText('POLYGON((-87.69227959522789 41.85766547551493,-87.69227959522789 41.88908028505862,-87.63450859376373 41.88908028505862,-87.63450859376373 41.85766547551493,-87.69227959522789 41.85766547551493))', 4326), shape_data.geometry)) as shared_area
                    FROM {SD_TABLE_NAME}
                    ORDER BY shared_area ASC;"""

    TASKS_PATHS = {
        "TASK_3_QUERY": (TASK_3_QUERY, output_path3),
        "TASK_4_QUERY": (TASK_4_QUERY, output_path4),
        "TASK_5_QUERY": (TASK_5_QUERY, output_path5),
        "TASK_6_QUERY": (TASK_6_QUERY, output_path6),
        "TASK_7_QUERY": (TASK_7_QUERY, output_path7),
        "TASK_8_QUERY": (TASK_8_QUERY, output_path8),
        "TASK_9_QUERY": (TASK_9_QUERY, output_path9),
        "TASK_10_QUERY": (TASK_10_QUERY, output_path10),
    }
    # ================= TASK 2 =================
    # CREATE TABLE
    cur.execute(TASK_2_QUERY)

    # LOAD LATITUDE AND LONGITUDE FROM IP FILE
    f = open(input_path)
    cur.copy_from(f, PT_TABLE_NAME, sep=",")
    connection.commit()

    # EXECUTE TASKS 3 - 10
    for key, value in TASKS_PATHS.items():
        query = value[0]
        outputPath = value[1]
        cur.execute(query)
        results = cur.fetchall()
        write_output(results, outputPath)


def write_output(results, output_path):
    f = open(output_path, "w")
    for values in results:
        f.write(str(values[0]) + "\n")
    f.close()
