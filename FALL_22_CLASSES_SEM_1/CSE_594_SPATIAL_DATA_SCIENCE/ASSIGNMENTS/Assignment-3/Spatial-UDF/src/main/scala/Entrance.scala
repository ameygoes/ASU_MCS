import org.apache.log4j.{Level, Logger}
import org.apache.sedona.sql.utils.SedonaSQLRegistrator
import org.apache.sedona.viz.core.Serde.SedonaVizKryoRegistrator
import org.apache.sedona.viz.sql.utils.SedonaVizRegistrator
import org.apache.spark.serializer.KryoSerializer
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.col
import org.locationtech.jts.geom._

import scala.Console.println
import scala.sys.process._


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



// DRIVER CODE - TAKES IN A INPUT AS STRING ENTERED FROM QUERY
//    ENTRY POINT OF THE CODE
  def Driver_Code(str: String): Geometry ={

//    GET GEOMETRY TYPE AND CALL FUNCTIONS ACCORDING TO GEOMETRY TYPE
      val geomType = str.split('(')(0).replace(" ","")
      println("Saving Geometry: " + geomType);

//    CALL POINT GEOM
      if (geomType == "POINT") {
        val data = str.split('(').apply(1).split(')').apply(0)
        return Point_From_String(data)
      }

//    CALL LINESTRING
      else if (geomType == "LINESTRING") {
        val data = str.split('(').apply(1).split(')').apply(0)
        return LineString_from_Text(data)
      }

      //    CALL POLYGON
      else if (geomType == "POLYGON") {
        val data = str.split('(').apply(2).split(')').apply(0)
        return Polygon_from_String(data)
      }

//       CALL MULTIPOLYGON
      else if (geomType == "MULTIPOLYGON") {
        return MultiPolygon_From_String(str)
      }

//        IF NOT ERROR OUT APPROPRITAE MESSAGE
      else {
        throw new Exception("Invalid Input String! String Must be in valid wkt format!")
      }
    }


//    THIS FUNCTIONS TAKES ARRAY OF STRING AS AN ARGUMENT
//    RETURNS ARRAY OF CO-ORDINATES
  def Get_Array_of_Coordinates(pointsArray: Array[String]): Array[Coordinate] = {

    var lineStringArray = Array[Coordinate]()
    for (i <- 0 until pointsArray.length) {
      lineStringArray = lineStringArray :+ Coordinate_From_String(pointsArray(i))
    }

    lineStringArray
  }

//    RETURNS THE CO-ORDINATE FROM POINT STRING
    def Coordinate_From_String(text: String): Coordinate = {
      val x = text.split(' ').apply(0)
      val y = text.split(' ').apply(1)
      val coordinate = new Coordinate()
      coordinate.x = x.toDouble
      coordinate.y = y.toDouble
      coordinate
    }

// THIS FUNCTION TAKES STRING AND RETURNS POINT OBJECT
    def Point_From_String(text: String): Point = {
      val coordinate = Coordinate_From_String(text)
      val point = new Point(coordinate, new PrecisionModel(), "0".toInt);
      point
    }

//    THIS FUNCTION TAKES STRING AND RETURNS LINESTRING OBJECT
    def LineString_from_Text(str:String): LineString ={
      //      GET THE SECOND ELEMENT OF SPLITTED ARRAY
      val pointsArray = str
        .replaceAll(", ", ",")
        .replaceAll(" ,", ",")
        .split(',')

      //      GET ARRAY OF CO-ORDINATES
      val coordinatePointArray = Get_Array_of_Coordinates(pointsArray)


      val LineStringObject = new LineString(coordinatePointArray, new PrecisionModel(), "0".toInt);
      LineStringObject
    }

//    THIS FUNCTION TAKES STRING AND RETURNS POLYGON OBJECT
    def Polygon_from_String(str: String): Polygon = {


      val pointsArray = str
        .replaceAll(", ", ",")
        .replaceAll(" ,", ",")
        .split(',')

      // GET ARRAY OF CO-ORDINATES
      val coordinatePointArray = Get_Array_of_Coordinates(pointsArray)

      val LinearRingObject = new LinearRing(coordinatePointArray, new PrecisionModel(), "0".toInt);
      val PolygonObject = new Polygon(LinearRingObject, new PrecisionModel(), "0".toInt);
      PolygonObject
    }

    //    THIS FUNCTION TAKES STRING AND RETURNS MULTIGON OBJECT
    def MultiPolygon_From_String(str: String): MultiPolygon ={
      var polygonArray = new Array[Polygon](0);

      val StrSplittedArray = str.split('(').filter(_.nonEmpty);
      for (i <- 1 until StrSplittedArray.length) {
        polygonArray = polygonArray:+ Polygon_from_String(StrSplittedArray(i).split(')').apply(0))
      }

      val multigonObject = new MultiPolygon(polygonArray, new PrecisionModel(), "0".toInt );

    multigonObject
    }


// REGISTER FUNCTION TO SPARK
    spark.udf.register("UDFGeomFromText", Driver_Code(_:String))

//    INITIALIZE SOME VARIABLES
//    val filePath = "data/inputs/test-data.csv"
    val filePath = "data/inputs/SDS_DataSet.csv"
    val outputPath = "data/outputs"
    val trueOutputPath = "data/true-outputs"

//    INITIALIZE CSV FILE READER WITH APPROPRIATE OPTIONS
    val CSVDatadf = spark.read.format("csv")
      .option("header", false)
      .option("delimiter", "\n")
      .option("multiLine", true)
      .load(filePath)

// ITERATE OVER CSV ROWS AND CALL INBUILT ST-FUNCTION AND UDF FUCNTIONS
// WRITE RESULTS TO PART FILES
     CSVDatadf.collect.foreach(f=> {
      val validStringInput = f.toString()
                              .replace("[","")
                              .replace("]","")
                              .replace("\"","")

//       VARIABLES FOR UDF COMPUTATION
      val QueryStringUDF = f"""Select UDFGeomFromText('$validStringInput') as UDFResults"""
      val UDFdf = spark.sql(QueryStringUDF).withColumn("UDFResults", col("UDFResults").cast("string"))

//       VARIABLES FOR INBUILT COMPUTATION
      val QueryString = f"""select ST_GeomFromText('$validStringInput') as InbuiltResults"""
      val df = spark.sql(QueryString).withColumn("InbuiltResults", col("InbuiltResults").cast("string"))

//       WRITE BOTH DF TO FILES
      df.repartition(1).write.mode("append").format("text").save(trueOutputPath)
      UDFdf.repartition(1).write.mode("append").format("text").save(outputPath)

    }
    )

    // YOU NEED TO FILL IN THIS USER DEFINED FUNCTION
    spark.udf.register("ST_Contains", (queryRectangle: String, pointString: String) => {

    val coOrdinates = queryRectangle.split(',')
    val xBL = coOrdinates.apply(0)
    val yBL = coOrdinates.apply(1)
    val xTR = coOrdinates.apply(2)
    val yTR = coOrdinates.apply(3)
    println(xBL, yBL, xTR, yTR)

    val pointCords = pointString.split(',')
    val xPC = pointCords.apply(0)
    val yPC = pointCords.apply(1)
    println(xPC, yPC)
    if (xPC >= xBL && xPC <= xTR && yPC >= yBL && yPC <= yTR) {
      true
    }


    false

   })

    //    CALL TO PYTHON SCRIPT TO COMPARE FILES
    CompareFiles()

    def CompareFiles(){
      val result = "python compareFiles.py".!!
        println(result)
    }

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
