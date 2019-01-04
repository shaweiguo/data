# -*- coding: utf-8 -*-
# ♂♀◆◇◎●★○☆△▲■□

import logging
import pika
from pyspark.sql import SparkSession

mq = None
channel = None

table_names = ['AppConfig', 'Application', 'APPMedicine', 'Medicine', 'Prescription', 'StdMedicine']
_rdds = {}
# _rdds = {
#     "AppCinfig": None,
#     "Application": None,
#     "AppMedicine": None,
#     "Medicine": None,
#     "Prescription": None,
#     "StdMedicine": None
# }


def callback(ch, method, properties, body):
    # logging.info(" [x] %r " % body)
    print(" [x] %r " % body)


def get_rdd(table_name):
    # pg_host = 'us'
    # pg_port = 5432
    # db_name = 'test'
    # pg_user = 'admin'
    # pg_password = 'Passw0rd'
    # url = "jdbc:postgresql://{host}:{port}/{db}".format(host=pg_host, port=pg_port, db=db_name)

    # uri = "mongodb://yb_admin:Q!W%40e3r4@us:27017/yb"
    # uri = "mongodb://yb_admin:q1w2e3r4@us:27017/yb"
    uri = "mongodb://root:q1w2e3r4@us:27017/yb"
    # df = spark.read.format("com.mongodb.spark.sql")\
    #     .option("uri", uri)\
    #     .option("collection", table_name)\
    #     .load()
    uri = uri + ".{}?authSource=admin&readPreference=primaryPreferred".format(table_name)
    # uri = uri + ".{}?authSource=yb&readPreference=primaryPreferred".format(table_name)
    print("++++++++++++++++++++++++++++++++++++++++++")
    print(uri)
    print("++++++++++++++++++++++++++++++++++++++++++")
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
        .option("uri", uri)\
        .load()
    return df


def init_rdds():
    global _rdds, table_names

    for table_name in table_names:
        _rdds[table_name] = None

    for table_name in table_names:
        _rdds[table_name] = get_rdd(table_name)

    for table_name in table_names:
        _rdds[table_name].show(20)


def update_rdd(table_name):
    global _rdds
    _rdds[table_name] = get_rdd(table_name)


def init():
    global mq, channel

    exchange_name = 'sanguo_topic'
    binding_key = "#"
    credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
    params = pika.ConnectionParameters('us', 5672, '/', credentials)
    try:
        mq = pika.BlockingConnection(params)
        channel = mq.channel()
        channel.exchange_declare(exchange=exchange_name,
                                 exchange_type='topic')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange_name,
                           queue=queue_name,
                           routing_key=binding_key)
        channel.basic_consume(callback,
                              queue=queue_name,
                              no_ack=True)
    except KeyboardInterrupt as e:
        mq.close()
        logging.error(e)
    except Exception as e:
        logging.error(e)


def main():
    global mq, channel

    try:
        init_rdds()
        # logging.info("Init completed.")
        print(' [*] Waiting for logs. To exit press CTRL+C')
        # channel.start_consuming()
    except KeyboardInterrupt:
        print("exit...")
        # mq.close()


if __name__ == "__main__":
    """
        Usage: 
    """
    spark = SparkSession\
        .builder\
        .appName("lz-engine")\
        .getOrCreate()

    main()

    spark.stop()
