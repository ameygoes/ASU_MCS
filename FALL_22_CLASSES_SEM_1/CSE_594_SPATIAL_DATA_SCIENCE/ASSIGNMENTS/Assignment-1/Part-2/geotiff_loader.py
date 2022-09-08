
from pyspark import StorageLevel
from pyspark.sql import SparkSession
from sedona.register import SedonaRegistrator
from sedona.utils import SedonaKryoRegistrator, KryoSerializer
import numpy as np
import task


spark = SparkSession.\
    builder.\
    master("local[*]").\
    appName("Sedona App").\
    config("spark.serializer", KryoSerializer.getName).\
    config("spark.kryo.registrator", SedonaKryoRegistrator.getName).\
    config("spark.jars.packages","org.apache.sedona:sedona-python-adapter-3.0_2.12:1.2.1-incubating,org.datasyslab:geotools-wrapper:1.1.0-25.2").\
    getOrCreate()


SedonaRegistrator.registerAll(spark)
sc = spark.sparkContext
sc.setSystemProperty("sedona.global.charset", "utf8")


DATA_DIR = "data/raster"


df = spark.read.format("geotiff").option("dropInvalid",True).option("readToCRS", "EPSG:4326").option("disableErrorInCRS", False).load(DATA_DIR)
df.printSchema()


df = df.selectExpr("image.origin as origin","ST_GeomFromWkt(image.geometry) as Geom", "image.height as height", "image.width as width", "image.data as data", "image.nBands as bands")
df.show(5)

npMax = task.get_bands_max(df)

with open('data/output/np_max.npy', 'wb') as f:
    np.save(f, npMax)
    print(npMax)





