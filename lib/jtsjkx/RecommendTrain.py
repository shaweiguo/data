# -*- coding: UTF-8 -*-
from pyspark.mllib.recommendation import ALS
# from common import Path, create_spark_context, set_logger, set_path
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


def create_spark_context():
    conf = SparkConf().setAppName("RecommendTrain").set("spark.ui.showConsoleProgress", "false")
    sc = SparkContext(conf=conf)

    print("master=" + sc.master)
    set_logger(sc)
    set_path(sc)

    return sc


def prepare_data(sc):
    print("读取用户评分数据...")
    rawUserData = sc.textFile(Path + "u.data")
    rawRatings = rawUserData.map(lambda line: line.split("\t")[:3])
    ratingsRDD = rawRatings.map(lambda x: (x[0], x[1], x[2]))

    numRatings = ratingsRDD.count()
    numUsers = ratingsRDD.map(lambda x: x[0]).distinct().count()
    numMovies = ratingsRDD.map(lambda x: x[1]).distinct().count()

    print("统计：")
    print("    评级数： " + str(numRatings))
    print("    用户数： " + str(numUsers))
    print("    电影总数： " + str(numMovies))

    return ratingsRDD


def save_model():
    try:
        model.save(sc, Path + 'ALSmodel')
        print('ALSmodel saved.')
    except Exception:
        print('model is exist, please delete it first.')


if __name__ == '__main__':
    sc = create_spark_context()

    print('========== data prepare =========')
    ratingsRDD = prepare_data(sc)
    print('========== train ==========')
    model = ALS.train(ratingsRDD, 5, 20, 0.1)
    print('========== save model ==========')
    save_model()
