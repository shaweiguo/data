# -*- coding: UTF-8 -*-
from pyspark import SparkConf, SparkContext


def set_logger(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)


def set_path(sc):
    global Path
    if sc.master[0:5]=="local":
        Path = "file:/home/sha/eclipse-workspace/SparkPrj/data/"
    else:
        Path = "hdfs://us:9000/user/sha/data/movies/ml-100k/"


def create_spark_context(app_name):
    conf = SparkConf().setAppName(app_name).set("spark.ui.showConsoleProgress", "false")
    sc = SparkContext(conf=conf)

    print("master=" + sc.master)
    set_logger(sc)
    set_path(sc)

    return sc
