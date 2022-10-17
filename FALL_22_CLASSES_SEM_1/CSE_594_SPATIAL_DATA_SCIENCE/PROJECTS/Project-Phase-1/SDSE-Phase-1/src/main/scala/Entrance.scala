import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import org.apache.spark.serializer.KryoSerializer
import org.apache.sedona.sql.utils.SedonaSQLRegistrator
import org.apache.sedona.viz.core.Serde.SedonaVizKryoRegistrator
import org.apache.sedona.viz.sql.utils.SedonaVizRegistrator


object Entrance extends App {
  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)

  override def main(args: Array[String]) {

    val spark: SparkSession = SparkSession.builder()
    .config("spark.serializer",classOf[KryoSerializer].getName)
    .config("spark.kryo.registrator", classOf[SedonaVizKryoRegistrator].getName)
    .master("local[*]")
    .appName("SDSE-Phase-1-Apache-Sedona")
    .getOrCreate()

    SedonaSQLRegistrator.registerAll(spark)
    SedonaVizRegistrator.registerAll(spark)

    val dfTrajecotry = ManageTrajectory.loadTrajectoryData(spark, "data/simulated_trajectories.json")

    paramsParser(spark, dfTrajecotry, args)

  }

  private def paramsParser(spark: SparkSession, dfTrajecotry: DataFrame, args: Array[String]): Unit = {
    var paramOffset = 1
    var currentQueryParams = ""
    var currentQueryName = ""
    var currentQueryIdx = -1

    while (paramOffset <= args.length) {
      if (paramOffset == args.length || args(paramOffset).toLowerCase.contains("get")) {
        // Turn in the previous query
        if (currentQueryIdx != -1) queryLoader(spark, dfTrajecotry, currentQueryName, currentQueryParams, args(0) + "/" + currentQueryName)

        // Start a new query call
        if (paramOffset == args.length) return

        currentQueryName = args(paramOffset)
        currentQueryParams = ""
        currentQueryIdx = currentQueryIdx + 1
      }
      else {
        // Keep appending query parameters
        currentQueryParams = currentQueryParams + args(paramOffset) + " "
      }
      paramOffset = paramOffset + 1
    }
  }

  private def queryLoader(spark: SparkSession, dfTrajecotry: DataFrame, queryName: String, queryParams: String, outputPath: String) {

    val queryParam = queryParams.split(" ")

    if (queryName.equalsIgnoreCase("get-spatial-range")) {
      if (queryParam.length != 4) throw new ArrayIndexOutOfBoundsException("Query " + queryName + " needs 4 parameter but you entered " + queryParam.length)
      ManageTrajectory.getSpatialRange(spark, dfTrajecotry, queryParam(0).toDouble, queryParam(1).toDouble, queryParam(2).toDouble, queryParam(3).toDouble).coalesce(1).write.mode(SaveMode.Overwrite).json(outputPath)
    }
    else if (queryName.equalsIgnoreCase("get-spatiotemporal-range")) {
      if (queryParam.length != 6) throw new ArrayIndexOutOfBoundsException("Query " + queryName + " needs 6 parameter but you entered " + queryParam.length)
      ManageTrajectory.getSpatioTemporalRange(spark, dfTrajecotry, queryParam(0).toLong, queryParam(1).toLong, queryParam(2).toDouble, queryParam(3).toDouble, queryParam(4).toDouble, queryParam(5).toDouble).coalesce(1).write.mode(SaveMode.Overwrite).json(outputPath)
    }
    else if (queryName.equalsIgnoreCase("get-knn")) {
      if (queryParam.length != 2) throw new ArrayIndexOutOfBoundsException("Query " + queryName + " needs 2 parameter but you entered " + queryParam.length)
      ManageTrajectory.getKNNTrajectory(spark, dfTrajecotry, queryParam(0).toLong, queryParam(1).toInt).coalesce(1).write.mode(SaveMode.Overwrite).json(outputPath)
    }
    else {
      throw new NoSuchElementException("The given query name " + queryName + " is wrong. Please check your input.")
    }

  }
}
