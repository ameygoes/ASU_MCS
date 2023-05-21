package cse511

object HotzoneUtils {

  def ST_Contains(queryRectangle: String, pointString: String ): Boolean = {

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
  }
}
