# -*- coding: utf-8 -*-
# ♂♀◆◇◎●★○☆△▲■□

import logging
import pika
from pyspark.sql import SparkSession

mq = None
channel = None


def callback(ch, method, properties, body):
    # logging.info(" [x] %r " % body)
    print(" [x] %r " % body)


def getDBTableDF(table_name):
    pg_host = 'us'
    pg_port = 5432
    db_name = 'test'
    pg_user = 'admin'
    pg_password = 'Passw0rd'

    url = "jdbc:postgresql://{host}:{port}/{db}".format(host=pg_host, port=pg_port, db=db_name)

    pgDF = spark.read.format("jdbc")\
        .option("driver", "org.postgresql.Driver")\
        .option("url", url)\
        .option("dbtable", table_name)\
        .option("user", pg_user)\
        .option("password", pg_password)\
        .load()
    return pgDF


def initDB():
    pgDF = getDBTableDF("public.person")
    pgDF.show()


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
        initDB()
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
