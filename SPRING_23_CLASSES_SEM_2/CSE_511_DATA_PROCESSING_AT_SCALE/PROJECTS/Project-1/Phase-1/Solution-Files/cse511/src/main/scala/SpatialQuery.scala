
package cse511

import org.apache.spark.sql.SparkSession

object SpatialQuery extends App{
  def runRangeQuery(spark: SparkSession, arg1: String, arg2: String): Long = {

	val pointDf = spark.read.format("com.databricks.spark.csv").option("delimiter","\t").option("header","false").load(arg1);
	pointDf.createOrReplaceTempView("point")


	// YOU NEED TO FILL IN THIS USER DEFINED FUNCTION
	spark.udf.register("ST_Contains",(queryRectangle:String, pointString:String)=>{
      
		// Rectangle Coordinates
		val coOrdinates = queryRectangle.split(',')
		val xBL = coOrdinates.apply(0).toFloat
		val yBL = coOrdinates.apply(1).toFloat
		val xTR = coOrdinates.apply(2).toFloat
		val yTR = coOrdinates.apply(3).toFloat

		// Point Coordinates
		val pointCords = pointString.split(',')
		val xPC = pointCords.apply(0).toFloat
		val yPC = pointCords.apply(1).toFloat
		
		var results = false	
		
		if (xPC >= xBL && xPC <= xTR && yPC >= yBL && yPC <= yTR) {
		  results = true
		}

		results

   })

	val resultDf = spark.sql("select * from point where ST_Contains('"+arg2+"',point._c0)")
	resultDf.show()

	return resultDf.count()
  }

  def runRangeJoinQuery(spark: SparkSession, arg1: String, arg2: String): Long = {

	val pointDf = spark.read.format("com.databricks.spark.csv").option("delimiter","\t").option("header","false").load(arg1);
	pointDf.createOrReplaceTempView("point")

	val rectangleDf = spark.read.format("com.databricks.spark.csv").option("delimiter","\t").option("header","false").load(arg2);
	rectangleDf.createOrReplaceTempView("rectangle")

	// YOU NEED TO FILL IN THIS USER DEFINED FUNCTION
	spark.udf.register("ST_Contains",(queryRectangle:String, pointString:String)=>{
      
		// Rectangle Coordinates
		val coOrdinates = queryRectangle.split(',')
		val xBL = coOrdinates.apply(0).toFloat
		val yBL = coOrdinates.apply(1).toFloat
		val xTR = coOrdinates.apply(2).toFloat
		val yTR = coOrdinates.apply(3).toFloat

		// Point Coordinates
		val pointCords = pointString.split(',')
		val xPC = pointCords.apply(0).toFloat
		val yPC = pointCords.apply(1).toFloat
		
		var results = false	
		
		if (xPC >= xBL && xPC <= xTR && yPC >= yBL && yPC <= yTR) {
		  results = true
		}

		results

   })

	val resultDf = spark.sql("select * from rectangle,point where ST_Contains(rectangle._c0,point._c0)")
	resultDf.show()

	return resultDf.count()
  }

  def runDistanceQuery(spark: SparkSession, arg1: String, arg2: String, arg3: String): Long = {

	val pointDf = spark.read.format("com.databricks.spark.csv").option("delimiter","\t").option("header","false").load(arg1);
	pointDf.createOrReplaceTempView("point")

	// YOU NEED TO FILL IN THIS USER DEFINED FUNCTION
	spark.udf.register("ST_Within",(pointString1:String, pointString2:String, distance:Double)=>({
			// Extract the 2 points from the strings
			val point1 = pointString1.split(',')
			val point2 = pointString2.split(',')

			//X and Y co-ordinates
			val p1x = point1.apply(0).toDouble
			val p1y = point1.apply(1).toDouble

			val p2x = point2.apply(0).toDouble
			val p2y = point2.apply(1).toDouble

			val x_distance = scala.math.pow((p2x - p1x), 2)
			val y_distance = scala.math.pow((p2y - p1y), 2)

			//Calculating Euclidean Distance
			val dist = scala.math.sqrt(x_distance + y_distance)
			var res = false

			if(dist <= distance){
				res = true
			}
			res
	})
	)

	val resultDf = spark.sql("select * from point where ST_Within(point._c0,'"+arg2+"',"+arg3+")")
	resultDf.show()

	return resultDf.count()
  }

  def runDistanceJoinQuery(spark: SparkSession, arg1: String, arg2: String, arg3: String): Long = {

	val pointDf = spark.read.format("com.databricks.spark.csv").option("delimiter","\t").option("header","false").load(arg1);
	pointDf.createOrReplaceTempView("point1")

	val pointDf2 = spark.read.format("com.databricks.spark.csv").option("delimiter","\t").option("header","false").load(arg2);
	pointDf2.createOrReplaceTempView("point2")

	// YOU NEED TO FILL IN THIS USER DEFINED FUNCTION
	spark.udf.register("ST_Within",(pointString1:String, pointString2:String, distance:Double)=>({
          val point1 = pointString1.split(",")
          val point2 = pointString2.split(",")

          val p1x = point1.apply(0).toDouble
          val p1y = point1.apply(1).toDouble

          val p2x = point2.apply(0).toDouble
          val p2y = point2.apply(1).toDouble

          val xdist = scala.math.pow((p2x - p1x), 2)
          val ydist = scala.math.pow((p2y - p1y), 2)

          val dist = scala.math.sqrt((xdist + ydist))

          var result = false

          if(distance >= dist){
            result = true
          }

          result
        })
        )

	val resultDf = spark.sql("select * from point1 p1, point2 p2 where ST_Within(p1._c0, p2._c0, "+arg3+")")
	resultDf.show()

	return resultDf.count()
  }
}
