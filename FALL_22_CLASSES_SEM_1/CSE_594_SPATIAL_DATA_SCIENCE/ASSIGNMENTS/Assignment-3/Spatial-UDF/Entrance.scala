import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import org.apache.spark.serializer.KryoSerializer
import org.apache.sedona.sql.utils.SedonaSQLRegistrator
import org.apache.sedona.viz.core.Serde.SedonaVizKryoRegistrator
import org.apache.sedona.viz.sql.utils.SedonaVizRegistrator
import org.locationtech.jts.geom.{Coordinate, Geometry, LineString, LinearRing, Point, Polygon, PrecisionModel, MultiPolygon}
import org.apache.spark.sql.functions.udf


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
    .appName("Spatial-UDF-Apache-Sedona")
    .getOrCreate()

    SedonaSQLRegistrator.registerAll(spark)
    SedonaVizRegistrator.registerAll(spark)





    def udf_WKT_reader(wkt:String):Geometry={
      val geometry_type = wkt.split('(').apply(0).replace(" ","")
      println(geometry_type)
      if(geometry_type == "POINT"){
        print("returning Point")
        val data = wkt.split('(').apply(1).split(')').apply(0)
        Point_From_String(data)
      }else if(geometry_type == "LINESTRING"){
        println("Returning Line string")
        val data = wkt.split('(').apply(1).split(')').apply(0)
         LineFromString(data)
      }else if(geometry_type == "POLYGON"){
        val data = wkt.split('(').apply(2)
        PolygonFromString(data)
      } else if(geometry_type == "MULTIPOLYGON"){
        println("Returning : "+ geometry_type)
        MultiPolygonFromString(wkt)
      }else{
        throw new Exception("Something went Wrong")
      }
    }

    //Coordinate from String
    def Coordinate_From_String(text: String): Coordinate = {
      val x = text.split(' ').apply(0)
      val y = text.split(' ').apply(1)
      val coordinate = new Coordinate()
      coordinate.x = x.toDouble;
      coordinate.y = y.toDouble;
      coordinate
    }

      // return the point given that the string is a point
      def Point_From_String(text: String): Point = {
        val coordinate = Coordinate_From_String(text)
        val point = new Point(coordinate, new PrecisionModel(), "0".toInt)
        point
      }


    // returns Linestring for the data given. The data is comma separated point values
    def LineFromString(datastr: String):LineString={
      var data = datastr.replaceAll(", ", ",")
      data = data.replaceAll(" ,", ",")

      val point_data = data.split(',')
      var points = new Array[Coordinate](0)
      for(point <- point_data){
        points = points :+ Coordinate_From_String(point)
      }
      val lineString = new LineString(points,new PrecisionModel(), "0".toInt)
      lineString
    }
    def PolygonFromString(datastr: String): Polygon ={
      var data = datastr.split('(').apply(0)
      data = data.split(')').apply(0)
      data = data.replaceAll(", ", ",")
      data = data.replaceAll(" ,", ",")
      val point_data = data.split(',')
      var points = new Array[Coordinate](0)
      for (point <- point_data) {
        points = points :+ Coordinate_From_String(point)
      }
      val linearRing = new LinearRing(points, new PrecisionModel(), "0".toInt)
      new Polygon(linearRing, linearRing.getPrecisionModel, linearRing.getSRID)

    }

    def MultiPolygonFromString(wkt: String): MultiPolygon ={
      var k = 3
      var polygons = new Array[Polygon](0);
      while(wkt.split('(').length > k ){
        polygons = polygons:+ PolygonFromString(wkt.split('(').apply(k).split(')').apply(0))
        k = k + 2
      }
      new MultiPolygon(polygons,new PrecisionModel(), "0".toInt)
    }


    //var res = spark.sql("select ST_GeomFromText('LINESTRING(7 -1, 7 6, 9 6, 9 1, 7 -1)') as g").show()
    //print(res)
    //var res1 = spark.sql("select ST_GeomFromText('POINT(7 -1)') as g2").show()

    //var r = spark.sql(" Select ST_GeomFromText('POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))') as g").show()
    //var p = Point_From_String("23.5 48.7")
    //println(p)
    //"MULTIPOLYGON (((180 -16.067132663642447, 180 -16.555216566639196, 179.36414266196414 -16.801354076946883, 178.72505936299711 -17.01204167436804, 178.59683859511713 -16.639150000000004, 179.0966093629971 -16.433984277547403, 179.4135093629971 -16.379054277547404, 180 -16.067132663642447)), ((178.12557 -17.50481, 178.3736 -17.33992, 178.71806 -17.62846, 178.55271 -18.15059, 177.93266000000003 -18.28799, 177.38146 -18.16432, 177.28504 -17.72465, 177.67087 -17.381140000000002, 178.12557 -17.50481)), ((-179.79332010904864 -16.020882256741224, -179.9173693847653 -16.501783135649397, -180 -16.555216566639196, -180 -16.067132663642447, -179.79332010904864 -16.020882256741224)))"

    //udf_WKT_reader("POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))")

    var r = spark.sql(" Select ST_GeomFromText('MULTIPOLYGON (((180 -16.067132663642447, 180 -16.555216566639196, 179.36414266196414 -16.801354076946883, 178.72505936299711 -17.01204167436804, 178.59683859511713 -16.639150000000004, 179.0966093629971 -16.433984277547403, 179.4135093629971 -16.379054277547404, 180 -16.067132663642447)), ((178.12557 -17.50481, 178.3736 -17.33992, 178.71806 -17.62846, 178.55271 -18.15059, 177.93266000000003 -18.28799, 177.38146 -18.16432, 177.28504 -17.72465, 177.67087 -17.381140000000002, 178.12557 -17.50481)), ((-179.79332010904864 -16.020882256741224, -179.9173693847653 -16.501783135649397, -180 -16.555216566639196, -180 -16.067132663642447, -179.79332010904864 -16.020882256741224)))') as g").show()
    spark.udf.register("getGeomFromText", udf_WKT_reader(_:String))
    var q1 = spark.sql("Select getGeomFromText('MULTIPOLYGON (((180 -16.067132663642447, 180 -16.555216566639196, 179.36414266196414 -16.801354076946883, 178.72505936299711 -17.01204167436804, 178.59683859511713 -16.639150000000004, 179.0966093629971 -16.433984277547403, 179.4135093629971 -16.379054277547404, 180 -16.067132663642447)), ((178.12557 -17.50481, 178.3736 -17.33992, 178.71806 -17.62846, 178.55271 -18.15059, 177.93266000000003 -18.28799, 177.38146 -18.16432, 177.28504 -17.72465, 177.67087 -17.381140000000002, 178.12557 -17.50481)), ((-179.79332010904864 -16.020882256741224, -179.9173693847653 -16.501783135649397, -180 -16.555216566639196, -180 -16.067132663642447, -179.79332010904864 -16.020882256741224)))') as g").show()
    var q2 = spark.sql(" Select getGeomFromText('POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))') as g2").show()
    var q3 = spark.sql("select ST_GeomFromText('POINT(7 -1)') as g3").show()
    var q4 = spark.sql("select ST_GeomFromText('LINESTRING(7 -1, 7 6, 9 6, 9 1, 7 -1)') as g").show()




    /*
    TO DO
    ...........
    Load the datasets (point/polygon/any geometry data/raster data)
    Define a scala function to perform the ST operation you selected in Excel sheet. The function accepts parameters and returns computed output
    Register the defined function on sparksql with the name available in Excel sheet
    create temporary views for the datasets you loaded previously. you can simplify the loaded data before creating temporary view
    write and run sql queries on the temporary view using the registered ST function
    write the sql output in the output folder
     */


  }



}
