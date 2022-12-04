/*
* Copyright (c) 11/25/2022 . Amey Bhilegaonkar. All rights reserved.
* AUTHOR: Amey Bhilegoankar
* PORTFOLIO: https://ameyportfolio.netlify.app/
* FILE CREATION DATE: 11/25/2022
*/
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import org.apache.spark.serializer.KryoSerializer
import org.apache.sedona.sql.utils.SedonaSQLRegistrator
import org.apache.sedona.viz.core.Serde.SedonaVizKryoRegistrator
import org.apache.sedona.viz.sql.utils.SedonaVizRegistrator

object sparkUtils {

  def getSparkSession(): SparkSession={
    val spark: SparkSession = SparkSession.builder()
    .config ("spark.serializer", classOf[KryoSerializer].getName)
    .config ("spark.kryo.registrator", classOf[SedonaVizKryoRegistrator].getName)
    .master ("local[*]")
    .appName ("SDSE-Phase-1-Apache-Sedona")
    .getOrCreate ()
    SedonaSQLRegistrator.registerAll (spark)
    SedonaVizRegistrator.registerAll (spark)

//    return spark session
    spark
  }

  def closeSparkSession(spark: SparkSession) {
    spark.stop
  }
}
