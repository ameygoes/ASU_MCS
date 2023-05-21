package cse511

import java.sql.Timestamp
import java.text.SimpleDateFormat
import java.util.Calendar

object HotcellUtils {
  val coordinateStep = 0.01

  def CalculateCoordinate(inputString: String, coordinateOffset: Int): Int =
  {
    // Configuration variable:
    // Coordinate step is the size of each cell on x and y
    var result = 0
    coordinateOffset match
    {
      case 0 => result = Math.floor((inputString.split(",")(0).replace("(","").toDouble/coordinateStep)).toInt
      case 1 => result = Math.floor(inputString.split(",")(1).replace(")","").toDouble/coordinateStep).toInt
      // We only consider the data from 2009 to 2012 inclusively, 4 years in total. Week 0 Day 0 is 2009-01-01
      case 2 => {
        val timestamp = HotcellUtils.timestampParser(inputString)
        result = HotcellUtils.dayOfMonth(timestamp) // Assume every month has 31 days
      }
    }
    return result
  }

  def timestampParser (timestampString: String): Timestamp =
  {
    val dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss")
    val parsedDate = dateFormat.parse(timestampString)
    val timeStamp = new Timestamp(parsedDate.getTime)
    return timeStamp
  }

  def dayOfYear (timestamp: Timestamp): Int =
  {
    val calendar = Calendar.getInstance
    calendar.setTimeInMillis(timestamp.getTime)
    return calendar.get(Calendar.DAY_OF_YEAR)
  }

  def dayOfMonth (timestamp: Timestamp): Int =
  {
    val calendar = Calendar.getInstance
    calendar.setTimeInMillis(timestamp.getTime)
    return calendar.get(Calendar.DAY_OF_MONTH)
  }

  def findWeightsOfAdjecentCells(maxX: Double, minX: Double, maxY: Double, minY: Double, maxZ: Int, minZ: Int, x: Double, y: Double, z: Int): Int =
  {
    var result = 26
    var difference = 9
  
    if(x == maxX || x == minX){
      result = result - difference
      difference = (difference * 2)/3
    }

    if(y == maxY || y == minY){
      result = result - difference
      difference = (difference * 2)/3
    }

    if(z == maxZ || z == minZ){
      result = result - difference
      difference = (difference * 2)/3
    }
    result
  }

  def getGScore(weights: Double, sumPickUps: Double, stdDeviation: Double, cellsCount: Double, overallAVGPickupsAcrossCells: Double): Double =
  {
    (sumPickUps - overallAVGPickupsAcrossCells*weights)/(stdDeviation * Math.sqrt((cellsCount*weights - (weights*weights))/(cellsCount-1.0)))
  }
  
}
