import org.apache.log4j.{Level, Logger}
import org.apache.sedona.core.formatMapper.shapefileParser.ShapefileReader
import org.apache.sedona.core.spatialRDD.SpatialRDD
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.locationtech.jts.geom.Geometry

object SpatialOp {

  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)

  def getMBR(spark: SparkSession, filePath: String): RDD[Double] = {
    var polyRdd = new SpatialRDD[Geometry]()
    polyRdd = ShapefileReader.readToGeometryRDD(spark.sparkContext, filePath)

    //TODO
    // transform the coordinate refrenece system of polyRdd from "epsg:2263" to "epsg:4326"
    polyRdd.CRSTransform("epsg:2263", "epsg:4326")


    val areaRdd = polyRdd.rawSpatialRDD.rdd.map(f => {
      //TODO
      // return the area of the minimum bounding rectangle or envelop
      // Gets an Envelope containing the minimum and maximum x and y values in this Geometry.
      // If the geometry is empty, an empty Envelope is returned.
      //The returned object is a copy of the one maintained internally, to avoid aliasing issues.
      // For best performance, clients which access this envelope frequently should cache the return value.
      //Returns: the envelope of this Geometry.
      // getArea() Returns the area of this Geometry\
      f.getEnvelope().getArea()

    })

    //  SCALA SYNTAX FOR RETURNING
    areaRdd

  }

}
