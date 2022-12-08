
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.functions.{col, collect_list, explode, sort_array}
import org.apache.spark.sql.{DataFrame, SparkSession}

object ManageTrajectory {

  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)


  def loadTrajectoryData(spark: SparkSession, filePath: String): DataFrame =
    {
      val df = spark.read.option("multiline", "true").json(filePath)

//       used to create or split an array or map DataFrame columns to rows
      val DFExploded = df.withColumn("trajectory_expanded", explode(df("trajectory"))).drop("trajectory")
      val expandedDF = DFExploded.withColumn("timestamp",col("trajectory_expanded.timestamp")).withColumn("location",col("trajectory_expanded.location")).drop("trajectory_expanded")

//      SEPERATE LATITUDE AND LONGITUDE AND STORE AS POINT FOR ST FUNCTIONS
      val finalTrajectoryData = expandedDF
        .withColumn("latitude",col("location").getItem(0))
        .withColumn("longitude",col("location").getItem(1))

//      CREATE  VIEW AND RETURN ALL COLS
      finalTrajectoryData.createOrReplaceTempView("finalTrajectoryData")


      var queryOutput = spark.sql("SELECT trajectory_id,vehicle_id,timestamp, location, ST_POINT(latitude, longitude) as geometry FROM finalTrajectoryData")
      queryOutput
    }


  def getSpatialRange(spark: SparkSession, dfTrajectory: DataFrame, latMin: Double, lonMin: Double, latMax: Double, lonMax: Double): DataFrame =
  {

//  CREATE OR REPLACE VIEW AGAIN
    dfTrajectory.createOrReplaceTempView("finalTrajectoryData")

    val queryOutput = spark.sql(f"SELECT * FROM finalTrajectoryData WHERE ST_Contains(ST_PolygonFromEnvelope($latMin,$lonMin,$latMax,$lonMax),finalTrajectoryData.geometry)")
    val output = queryOutput.groupBy("trajectory_id","vehicle_id").agg(sort_array(collect_list("timestamp")).alias("timestamp"), collect_list("location").alias("location"))
    output.show()
    output

  }


  def getSpatioTemporalRange(spark: SparkSession, dfTrajectory: DataFrame, timeMin: Long, timeMax: Long, latMin: Double, lonMin: Double, latMax: Double, lonMax: Double): DataFrame =
  {
    dfTrajectory.createOrReplaceTempView("finalTrajectoryData")
    val queryOutput = spark.sql(f"SELECT * FROM finalTrajectoryData WHERE ST_Contains(ST_PolygonFromEnvelope($latMin,$lonMin,$latMax,$lonMax),finalTrajectoryData.geometry) AND timestamp BETWEEN $timeMin AND $timeMax")
    val output = queryOutput.groupBy("trajectory_id","vehicle_id").agg(sort_array(collect_list("timestamp")).alias("timestamp"), collect_list("location").alias("location"))
    output.show()
    output
  }


  def getKNNTrajectory(spark: SparkSession, dfTrajectory: DataFrame, trajectoryId: Long, neighbors: Int): DataFrame =
  {
    val data = dfTrajectory.groupBy("trajectory_id","vehicle_id").agg(collect_list("geometry").alias("geometry"))
    data.createOrReplaceTempView("finalTrajectoryData")

    val queryOutput = spark.sql("SELECT trajectory_id, ST_Collect(geometry) as geom FROM finalTrajectoryData")
    queryOutput.createOrReplaceTempView("tmp")

    val queryOutput2 = spark.sql(s"SELECT b.trajectory_id FROM tmp as a, tmp as b WHERE a.trajectory_id = $trajectoryId AND a.trajectory_id != b.trajectory_id ORDER BY (ST_DISTANCE(a.geom,b.geom)) LIMIT $neighbors")
    queryOutput2.show()
    queryOutput2
  }


}
