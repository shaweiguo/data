# -*- coding: UTF-8 -*-
import sys
from pyspark import SparkConf, SparkContext
from pyspark.mllib.recommendation import MatrixFactorizationModel


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
    conf = SparkConf().setAppName("Recommend").set("spark.ui.showConsoleProgress", "false")
    sc = SparkContext(conf=conf)

    print("master=" + sc.master)
    set_logger(sc)
    set_path(sc)

    return sc


def prepare_data(sc):
    print("读取电影ID与名称字典...")
    item_rdd = sc.textFile(Path + "u.item")
    movie_title = item_rdd.map(lambda line: line.split("|")).map(lambda a: (int(a[0]), a[1])).collectAsMap()

    return movie_title


def recommend_movies(model, movie_title, user_id):
    movies = model.recommendProducts(user_id, 10)

    print("对用户" + str(user_id) + "推荐以下电影：")

    for movie in movies:
        print("电影：{0}, 评分： {1}".format(movie_title[movie[1]], movie[2]))


def recommend_users(model, movie_title, movie_id):
    users = model.recommendUsers(movie_id, 10)

    print("推荐以下用户观看电影{0}：".format(movie_title[movie_id]))

    for user in users:
        print("用户: {0}，评分: {1}".format(user[0], user[2]))


def load_model(sc):
    try:
        print("加载模型...")
        model = MatrixFactorizationModel.load(sc, Path + "ALSmodel")
    except Exception:
        print("模型不存在！")

    return model


def recommend():
    sc = create_spark_context()
    print('========== 数据准备 =========')
    movie_title = prepare_data(sc)

    print("==========载入模型===============")
    model = load_model(sc)

    print("==========进行推荐===============")
    if sys.argv[1] == "--U":
        recommend_movies(model, movie_title, int(sys.argv[2]))
    if sys.argv[1] == "--M":
        recommend_users(model, movie_title, int(sys.argv[2]))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("请输入2个参数！")
        exit(-1)

    recommend()
