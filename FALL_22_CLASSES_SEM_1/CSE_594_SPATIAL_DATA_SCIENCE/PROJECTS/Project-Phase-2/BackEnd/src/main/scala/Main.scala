/*
* Copyright (c) 11/24/2022 . Amey Bhilegaonkar. All rights reserved.
* AUTHOR: Amey Bhilegoankar
* PORTFOLIO: https://ameyportfolio.netlify.app/
* FILE CREATION DATE: 11/24/2022
*/
// ================== backend imports ====================
import akka.actor.typed.scaladsl.Behaviors
import akka.http.scaladsl.Http
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.Route
import com.typesafe.config._
import akka.actor.{ActorSystem, typed}
import org.apache.spark.sql
//val config = ConfigFactory.load().withValue("akka.loglevel", ConfigValueFactory.fromAnyRef("OFF"))
//  .withValue("akka.stdout-loglevel", ConfigValueFactory.fromAnyRef("OFF"))



import java.nio.file.{Files, Paths}
// ================== JSON UTILS Imports =======================
import spray.json._
//import org.bson.Document
//implicit val system = ActorSystem("AlwaysNameYourSystem", config)


/* DEFINITION OF TRAJECTORY TO BE ADDED OBJECT
* STRUCTURE:
*   TRAJECTORY_ID
*   VEHICLE_ID
*   TRAJECTORY:
*       LOCATION:
*         LAT
*         LONGI
*       TIMESTAMP
*/
case class Location(
                     location: List[Double]
                   )
case class SingleLocationTimestamp(
                                    location: Location,
                                    timestamp: Long
                                  )
case class TrajectoryAdded(
                            trajectory_id: Int,
                            vehicle_id: Int,
                            trajectory: List[SingleLocationTimestamp],

                          )
case class TrajectoryArray(
                            trajectory: List[TrajectoryAdded]
                          )
case class Load(
              path: String
              )

case class GetSpartialRange(
                             latMin : Double,
                             lonMin : Double,
                             latMax : Double,
                             lonMax : Double
                           )

case class GetSpatioTemporalRange(
                             timeMin: Long,
                             timeMax: Long,
                             latMin : Double,
                             lonMin : Double,
                             latMax : Double,
                             lonMax : Double
                           )
case class GetKnn(
                   trajectoryId: Long,
                   neighbors: Int
                 )
// STEP - 2
trait TrajectoryJsonProtocol extends DefaultJsonProtocol{
  implicit val LocationFormat = jsonFormat1(Location)
  implicit val SingleLocationTimestampFormat = jsonFormat2(SingleLocationTimestamp)
  implicit val TrajectoryAddedFormat = jsonFormat3(TrajectoryAdded)
  implicit val TrajectoryArrayFormat = jsonFormat1(TrajectoryArray)
  implicit val Loadformats = jsonFormat1(Load)
  implicit val GSRformats = jsonFormat4(GetSpartialRange)
  implicit val GSTRformats = jsonFormat6(GetSpatioTemporalRange)
  implicit val GKnnformats = jsonFormat2(GetKnn)
  var pathJson : String
//  var dfTrajectory : sql.DataFrame
  var OutputPath : String

}


object Main extends TrajectoryJsonProtocol with SprayJsonSupport {
//  case class Person(name: String, age: Int)
implicit val system = typed.ActorSystem(Behaviors.empty, "AkkaHttpJson")

//  ================== DEFINE ROUTES =======================

  val load: Route = (path("api" / "load") & post) {
    entity(as[JsValue]) { json =>
      val inputFilePath = json.asJsObject.fields("path").toString().replace("\"","")
      if (Files.exists(Paths.get(inputFilePath))) {
          pathJson = inputFilePath
          complete(pathJson)
//        //    GET SPARK SESSION
//        val spark = sparkUtils.getSparkSession()
//
//        //    LOAD TRAJECTORY DATA
//        val dfTrajectory = ManageTrajectory.loadTrajectoryData(spark, pathJson)
//        val dfJson = dfTrajectory.toJSON.collect()
//        dfJson.toString()
//        sparkUtils.closeSparkSession(spark)
//        complete(dfJson)
      }
      else {
        complete("File Path Doesn't Exists: " + inputFilePath)
      }
    }
  }

  val gsr: Route = (path("api" / "gsr") & post) {
      entity(as[JsValue]) { json =>
        val latMin  = json.asJsObject.fields("latMin").toString().toDouble
        val lonMin  = json.asJsObject.fields("lonMin").toString().toDouble
        val latMax  = json.asJsObject.fields("latMax").toString().toDouble
        val lonMax  = json.asJsObject.fields("lonMax").toString().toDouble

        //    GET SPARK SESSION
        val spark = sparkUtils.getSparkSession()
        //    LOAD TRAJECTORY DATA
//        complete(pathJson)
        val dfTrajecotry = ManageTrajectory.loadTrajectoryData(spark, pathJson)
        val spr = ManageTrajectory.getSpatialRange(spark, dfTrajecotry, latMin, lonMin, latMax, lonMax)

//        SAVE FILE - Uncomment if needed
//        spr.write.mode(SaveMode.Overwrite).json(OutputPath)
        val dfJson = spr.toJSON.collect()
        dfJson.toString()

        sparkUtils.closeSparkSession(spark)
        complete(dfJson)

    }
  }

  val gstr: Route = (path("api" / "gstr") & post) {
    entity(as[JsValue]) { json =>
      val timeMin = json.asJsObject.fields("timeMin").toString().toLong
      val timeMax = json.asJsObject.fields("timeMax").toString().toLong
      val latMin = json.asJsObject.fields("latMin").toString().toDouble
      val lonMin = json.asJsObject.fields("lonMin").toString().toDouble
      val latMax = json.asJsObject.fields("latMax").toString().toDouble
      val lonMax = json.asJsObject.fields("lonMax").toString().toDouble

      //    GET SPARK SESSION
      val spark = sparkUtils.getSparkSession()
      //    LOAD TRAJECTORY DATA
      val dfTrajecotry = ManageTrajectory.loadTrajectoryData(spark, pathJson)
      val sptr = ManageTrajectory.getSpatioTemporalRange(spark, dfTrajecotry, timeMin, timeMax, latMin, lonMin, latMax, lonMax)

      //        SAVE FILE - Uncomment if needed
      //        sptr.write.mode(SaveMode.Overwrite).json(OutputPath)
      val dfJson = sptr.toJSON.collect()
      dfJson.toString()

      sparkUtils.closeSparkSession(spark)
      complete(dfJson)
    }
  }

  val gknn: Route = (path("api" / "gknn") & post) {
    entity(as[JsValue]) { json =>
      val trajectoryId = json.asJsObject.fields("trajectoryId").toString().toLong
      val neighbors = json.asJsObject.fields("neighbors").toString().toInt


      //    GET SPARK SESSION
      val spark = sparkUtils.getSparkSession()
      //    LOAD TRAJECTORY DATA
      val dfTrajecotry = ManageTrajectory.loadTrajectoryData(spark, pathJson)
      val gknn = ManageTrajectory.getKNNTrajectory(spark, dfTrajecotry, trajectoryId, neighbors)

      //        SAVE FILE - Uncomment if needed
      //        gknn.write.mode(SaveMode.Overwrite).json(OutputPath)
      val dfJson = gknn.toJSON.collect()
      dfJson.toString()

      sparkUtils.closeSparkSession(spark)
      complete(dfJson)
    }
  }


  def main(args: Array[String]): Unit = {
    Http().newServerAt("localhost", 8081).bind(load)
    Http().newServerAt("localhost", 8082).bind(gsr)
    Http().newServerAt("localhost", 8083).bind(gstr)
    Http().newServerAt("localhost", 8084).bind(gknn)
  }

  def loadFIle(): sql.DataFrame = {
      val spark = sparkUtils.getSparkSession()
      val dfTrajectory = ManageTrajectory.loadTrajectoryData(spark, pathJson)
      sparkUtils.closeSparkSession(spark)
      dfTrajectory
  }

  override var pathJson: String = "data/simulated_trajectories.json"
  override var OutputPath : String = "data/output"
//  override var dfTrajectory: sql.DataFrame = loadFIle()

}