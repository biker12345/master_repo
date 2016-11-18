name := "twitter_streaming"
version := "1.0.0"
scalaVersion := "2.11.8"
val sparkVersion = "2.0.1"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-streaming" % sparkVersion,
  "org.apache.spark" %% "spark-streaming-twitter" % "1.6.2"
 )


