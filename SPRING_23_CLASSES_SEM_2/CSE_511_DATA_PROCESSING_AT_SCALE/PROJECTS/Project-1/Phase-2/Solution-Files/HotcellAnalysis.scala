package cse511

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.functions._

object HotcellAnalysis {
  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)

    def runHotcellAnalysis(spark: SparkSession, pointPath: String): DataFrame = {
    
	// Load the original data from a data source
    var pickupInfo = spark.read.format("com.databricks.spark.csv").option("delimiter",";").option("header","false").load(pointPath);
    pickupInfo.createOrReplaceTempView("nyctaxitrips")
    pickupInfo.show()

    // Assign cell coordinates based on pickup points
    spark.udf.register("CalculateX",(pickupPoint: String)=>((
		HotcellUtils.CalculateCoordinate(pickupPoint, 0)
	)))
    
	spark.udf.register("CalculateY",(pickupPoint: String)=>((
		HotcellUtils.CalculateCoordinate(pickupPoint, 1)
    )))
    
	spark.udf.register("CalculateZ",(pickupTime: String)=>((
		HotcellUtils.CalculateCoordinate(pickupTime, 2)
    )))
    
	pickupInfo = spark.sql("select CalculateX(nyctaxitrips._c5),CalculateY(nyctaxitrips._c5), CalculateZ(nyctaxitrips._c1) from nyctaxitrips")
    var newCoordinateName = Seq("x", "y", "z")
    pickupInfo = pickupInfo.toDF(newCoordinateName:_*)
    pickupInfo.show()

    // Define the min and max of x, y, z
    val minX = -74.50/HotcellUtils.coordinateStep
    val maxX = -73.70/HotcellUtils.coordinateStep
    val minY = 40.50/HotcellUtils.coordinateStep
    val maxY = 40.90/HotcellUtils.coordinateStep
    val minZ = 1
    val maxZ = 31
    val numCells = (maxX - minX + 1)*(maxY - minY + 1)*(maxZ - minZ + 1)

    // YOU NEED TO CHANGE THIS PART
    val cellsCount = numCells.toDouble

	pickupInfo.createOrReplaceTempView("pickupInfoView")

	val countsByCell = spark.sql("""SELECT x, y, z, COUNT(*) as totalPickUpsInaCellOnaDay 
							    FROM pickupInfoView 
							    WHERE x BETWEEN %f AND %f 
							    AND y BETWEEN %f AND %f 
							    AND z BETWEEN %d AND %d 
							    GROUP BY x, y, z""".format(minX, maxX, minY, maxY, minZ, maxZ))

	countsByCell.createOrReplaceTempView("countsByCellView")

	val SumOftotalPickUpsInaCellOnaDay = spark.sql("SELECT SUM(totalPickUpsInaCellOnaDay), SUM(totalPickUpsInaCellOnaDay*totalPickUpsInaCellOnaDay) FROM countsByCellView")

	val overallAVGPickupsAcrossCells = SumOftotalPickUpsInaCellOnaDay.head().get(0).toString.toDouble / cellsCount

	val stdDeviation = Math.sqrt((SumOftotalPickUpsInaCellOnaDay.head().get(1).toString.toDouble / cellsCount) - (overallAVGPickupsAcrossCells * overallAVGPickupsAcrossCells))

	spark.udf.register("findWeightsOfAdjecentCells", (maxX: Double, minX: Double, maxY: Double, minY: Double, maxZ: Int, minZ: Int, x: Double, y: Double, z: Int) => {
	HotcellUtils.findWeightsOfAdjecentCells(maxX, minX, maxY, minY, maxZ, minZ, x, y, z)
	})

	val WiXi = spark.sql("""SELECT findWeightsOfAdjecentCells(%f, %f, %f, %f, %d, %d, view_1.x, view_1.y, view_1.z) as Wij, 
			     		  SUM(view_2.totalPickUpsInaCellOnaDay) as Xj, 
			     		  view_1.x as X, view_1.y as Y, view_1.z as Z
			     		  FROM countsByCellView view_1 JOIN countsByCellView view_2  
 			     		  ON (view_2.x = view_1.x OR view_2.x = view_1.x + 1 OR view_2.x = view_1.x - 1) 
			    	 	  AND (view_2.y = view_1.y OR view_2.y = view_1.y + 1 OR view_2.y = view_1.y - 1) 
			     		  AND (view_2.z = view_1.z OR view_2.z = view_1.z + 1 OR view_2.z = view_1.z - 1) 
			     		  GROUP BY view_1.x, view_1.y, view_1.z"""
					 .format(maxX, minX, maxY, minY, maxZ, minZ))

	WiXi.createOrReplaceTempView("WiXiValuesView")

	spark.udf.register("getGScore", (weights: Double, sumPickUps: Double, stdDeviation: Double, cellsCount: Double, overallAVGPickupsAcrossCells: Double) => {
	HotcellUtils.getGScore(weights, sumPickUps, stdDeviation, cellsCount, overallAVGPickupsAcrossCells)
	})

	val GScoreAnswers = spark.sql("""SELECT x, y, z, getGScore(Wij, Xj, %f, %f, %f) as GScore 
								FROM WiXiValuesView"""
								.format(stdDeviation, cellsCount, overallAVGPickupsAcrossCells))

	GScoreAnswers.createOrReplaceTempView("GScoreView")

	val result = spark.sql("""SELECT x, y, z 
							  FROM GScoreView 
							  ORDER BY GScore 
							  DESC LIMIT 50""")

	return result

}

}
