# -*- coding: UTF-8 -*-
from pyspark import SparkContext
from pyspark import SparkConf


def CreateSparkContext():
    sparkConf = SparkConf().setAppName("Word Counter").set("spark.ui.showConsoleProgress", "false")
    sc = SparkContext(conf=sparkConf)
    
    
    print("master=" + sc.master)
    SetLogger(sc)
    SetPath(sc)
    return sc


def SetLogger(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)


def SetPath(sc):
    global Path
    if sc.master[0:5] == "local":
        Path = "file:/home/sha/eclipse-workspace/SparkPrj/"
    else:
        Path = "hdfs://us:9000/user/sha/"


# spark-submit --master spark://us:7077 --deploy-mode client --executor-memory 512M --total-executor-cores 2 \
#  lib/jtsjkx/WordCount.py
if __name__ == "__main__":
    print("Word Counter running...")
    sc = CreateSparkContext()
    
    print("Reading text file...")
    textFile = sc.textFile(Path + "data/README.md")
    print("Readed " + str(textFile.count()) + " lines.")
    
    countsRDD = textFile.flatMap(lambda line: line.split(' ')).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
    print("Total is " + str(countsRDD.count()))
    
    print("Saving RDD...")
    try:
        countsRDD.saveAsTextFile(Path + "data/output")
    except Exception as e:
        print("Directory is already exist, please delete it first.")
    
    sc.stop()

    




