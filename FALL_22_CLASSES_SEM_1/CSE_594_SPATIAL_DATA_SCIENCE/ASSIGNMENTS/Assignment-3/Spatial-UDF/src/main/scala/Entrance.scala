import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import org.apache.spark.serializer.KryoSerializer
import org.apache.sedona.sql.utils.SedonaSQLRegistrator
import org.apache.sedona.viz.core.Serde.SedonaVizKryoRegistrator
import org.apache.sedona.viz.sql.utils.SedonaVizRegistrator
import org.apache.spark.sql.functions.udf
import org.locationtech.jts.geom.{Coordinate, Geometry, LineString, LinearRing, Point, Polygon, PrecisionModel}
import org.apache.sedona.core.spatialRDD.PointRDD



object Entrance extends App {
  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)

  override def main(args: Array[String]) {

    val spark: SparkSession = SparkSession.builder()
      .config("spark.serializer", classOf[KryoSerializer].getName)
      .config("spark.kryo.registrator", classOf[SedonaVizKryoRegistrator].getName)
      .master("local[*]")
      .appName("Spatial-UDF-Apache-Sedona")
      .getOrCreate()

    SedonaSQLRegistrator.registerAll(spark)
    SedonaVizRegistrator.registerAll(spark)

    def Get_Array_of_Coordinates(pointsArray: Array[String]): Array[Coordinate] ={

      var lineStringArray = Array[Coordinate]()
      for (i <- 0 until pointsArray.length) {
        lineStringArray = lineStringArray :+ Coordinate_From_String(pointsArray(i))
      }

      return lineStringArray
    }
// FIRST RETURN VALUE OF THIS ARRAY IS GEOM-TYPE
//    AND SECOND VALUE IS COMMA SEPERATED STRING OF POINTS
    def Get_Geom_Type_And_Value(str: String): Array[String] ={

      var ansArray = Array[String]()

      val geomType = str.split('(')(0)

      if(geomType == "POINT" || geomType == "LINESTRING"){
        val arr = str.split('(')
        ansArray = ansArray :+ geomType

        // GET THE SECOND ELEMENT OF SPLITTED ARRAY
        ansArray = ansArray :+ arr(1).split(')')(0)
      }

      if(geomType == "POLYGON" || geomType == "MULTIPOLYGON") {
          val arr = str.split('(')
        for (i <- 0 until pointsArray.length) {
          ansArray = ansArray :+ geomType
        arr(1).split(')')
      }

      return ansArray
    }

//    RETURNS THE CO-ORDINATE FROM POINT STRING
    def Coordinate_From_String(text: String): Coordinate = {
      var x = text.split(' ').apply(0)
      var y = text.split(' ').apply(1)
      var coordinate = new Coordinate()
      coordinate.x = x.toDouble
      coordinate.y = y.toDouble
      return coordinate
    }


    def Point_From_String(text: String): Point = {
      var coordinate = Coordinate_From_String(text)
      var point = new Point(coordinate, new PrecisionModel(), "0".toInt);
      return point
    }

    def LineString_from_Text(str:String): LineString ={

//      SPLIT LINESTRING WITH ( TO GET GEOM TYPE
//      TO BE CHANGED WITH THE UTILITY FUNCTION
      val GeomTypeValue = Get_Geom_Type_And_Value(str)
      var geomType = GeomTypeValue(0)

//      GET THE SECOND ELEMENT OF SPLITTED ARRAY
      var pointsArray = GeomTypeValue(1)
        .replaceAll(", ", ",")
        .replaceAll(" ,", ",")
        .split(',')

//      GET ARRAY OF CO-ORDINATES
      var coordinatePointArray = Get_Array_of_Coordinates(pointsArray)


      var LineStringObject = new LineString(coordinatePointArray, new PrecisionModel(), "0".toInt);
      println(LineStringObject)
      return LineStringObject
    }


    def Polygon_from_String(str: String): Polygon = {

      //      SPLIT LINESTRING WITH ( TO GET GEOM TYPE
      //      TO BE CHANGED WITH THE UTILITY FUNCTION
      val GeomTypeValue = Get_Geom_Type_And_Value(str)
      var geomType = GeomTypeValue(0)

      //      GET THE SECOND ELEMENT OF SPLITTED ARRAY
      var pointsArray = GeomTypeValue(1)
        .replaceAll(", ", ",")
        .replaceAll(" ,", ",")
        .split(',')

      //      GET ARRAY OF CO-ORDINATES
      var coordinatePointArray = Get_Array_of_Coordinates(pointsArray)


      var LinearRingObject = new LinearRing(coordinatePointArray, new PrecisionModel(), "0".toInt);
      var PolygonObject = new Polygon(LinearRingObject, new PrecisionModel(), "0".toInt);
      println(PolygonObject)
      return PolygonObject
    }


//    LineString_from_Text("LINESTRING(10 160,60 120,120 140,180 120)")
    Polygon_from_String("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))")
    POINT(0 0)




    /*
    TO DO
    ...........
    Load the datasets (point/polygon/any geometry data/raster data)
    Define a scala function to perform the ST operation you selected in Excel sheet.
    The function accepts parameters and returns computed output
    Register the defined function on sparksql with the name available in Excel sheet
    create temporary views for the datasets you loaded previously. you can simplify the loaded data before creating temporary view
    write and run sql queries on the temporary view using the registered ST function
    write the sql output in the output folder
     */


  }



}
