/*
* Copyright (c) 10/1/2022 . Amey Bhilegaonkar. All rights reserved.
* AUTHOR: Amey Bhilegoankar
* PORTFOLIO: https://ameyportfolio.netlify.app/
* FILE CREATION DATE: 10/1/2022
*/
class Test {
  import org.apache.spark.sql.SparkSession
  import org.apache.spark.sql.functions.udf

  val spark = SparkSession
    .builder()
    .appName("Spark SQL UDF scalar example")
    .getOrCreate()

  // Define and register a zero-argument non-deterministic UDF
  // UDF is deterministic by default, i.e. produces the same result for the same input.
  val random = udf(() => Math.random())
  spark.udf.register("random", random.asNondeterministic())
  spark.sql("SELECT random()").show()
  // +-------+
  // |UDF()  |
  // +-------+
  // |xxxxxxx|
  // +-------+

  // Define and register a one-argument UDF
  val plusOne = udf((x: Int) => x + 1)
  spark.udf.register("plusOne", plusOne)
  spark.sql("SELECT plusOne(5)").show()
  // +------+
  // |UDF(5)|
  // +------+
  // |     6|
  // +------+

  // Define a two-argument UDF and register it with Spark in one step
  spark.udf.register("strLenScala", (_: String).length + (_: Int))
  spark.sql("SELECT strLenScala('test', 1)").show()
  // +--------------------+
  // |strLenScala(test, 1)|
  // +--------------------+
  // |                   5|
  // +--------------------+

  // UDF in a WHERE clause
  spark.udf.register("oneArgFilter", (n: Int) => { n > 5 })
  spark.range(1, 10).createOrReplaceTempView("test")
  spark.sql("SELECT * FROM test WHERE oneArgFilter(id)").show()
}
