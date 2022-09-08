import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import org.apache.spark.serializer.KryoSerializer
import org.apache.sedona.sql.utils.SedonaSQLRegistrator
import org.apache.sedona.viz.core.Serde.SedonaVizKryoRegistrator
import org.apache.sedona.viz.sql.utils.SedonaVizRegistrator

import java.io.File
import scala.reflect.io.Directory

object Entrance extends App {
  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)

  override def main(args: Array[String]) {

    var spark: SparkSession = SparkSession.builder()
    .config("spark.serializer",classOf[KryoSerializer].getName)
    .config("spark.kryo.registrator", classOf[SedonaVizKryoRegistrator].getName)
    .master("local[*]")
    .appName("Spatial-Operations-Apache-Sedona")
    .getOrCreate()

    SedonaSQLRegistrator.registerAll(spark)
    SedonaVizRegistrator.registerAll(spark)

    paramsParser(spark, args)
  }

  private def paramsParser(spark: SparkSession, args: Array[String]): Unit = {
    var paramOffset = 1
    var currentQueryParams = ""
    var currentQueryName = ""
    var currentQueryIdx = -1

    while (paramOffset <= args.length) {
      if (paramOffset == args.length || args(paramOffset).toLowerCase.contains("get")) {
        // Turn in the previous query
        if (currentQueryIdx != -1) queryLoader(spark, currentQueryName, currentQueryParams, args(0) + currentQueryIdx)

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

  private def queryLoader(spark: SparkSession, queryName: String, queryParams: String, outputPath: String) {
    val dir = new Directory(new File(outputPath))
    dir.deleteRecursively()

    val queryParam = queryParams.split(" ")
    if (queryName.equalsIgnoreCase("get-mbr")) {
      if (queryParam.length != 1) throw new ArrayIndexOutOfBoundsException("Query " + queryName + " needs 1 parameter but you entered " + queryParam.length)
      SpatialOp.getMBR(spark, queryParam(0)).coalesce(1).saveAsTextFile(outputPath)
    }
    else {
      throw new NoSuchElementException("The given query name " + queryName + " is wrong. Please check your input.")
    }
  }
}
