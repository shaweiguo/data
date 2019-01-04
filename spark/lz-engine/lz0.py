# -*- coding: utf-8 -*-
# ♂♀◆◇◎●★○☆△▲■□

import logging
import pika
import json
from pyspark.sql import SparkSession

mq = None
ch_recommend_request = None
ch_db_changed = None

ex_recommend_request = 'sflz.ex.intelligent.recommend'
bk_recommend_request = "sflz.rk.intelligent.recommend"
ex_db_changed = 'sflz.ex.changedb'
bk_db_changed = "sflz.rk.changedb.notification"


def cb_recommend_request(ch, method, properties, body):
    # logging.info(" [x] %r " % body)
    print(" [x] %r " % body)


def cb_db_changed(ch, method, properties, body):
    # logging.info(" [x] %r " % body)
    print(" [x] %r:%r" % (method.routing_key, body))
    msg = body.decode('utf-8')
    print(msg)
    db_changed = json.loads(body.decode('utf-8'))
    print(db_changed)
    print(db_changed.keys())
    print(db_changed.values())


def init_mq():
    global mq, ch_recommend_request, ch_db_changed
    global ex_recommend_request, ex_db_changed
    global bk_recommend_request, bk_db_changed

    credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
    params = pika.ConnectionParameters('us', 5672, '/', credentials)

    try:
        mq = pika.BlockingConnection(params)
        ch_recommend_request = mq.channel()
        ch_recommend_request.exchange_declare(exchange=ex_recommend_request,
                                              exchange_type='topic')
        result = ch_recommend_request.queue_declare(exclusive=True)
        queue_name = result.method.queue
        ch_recommend_request.queue_bind(exchange=ex_recommend_request,
                                        queue=queue_name,
                                        routing_key=bk_recommend_request)
        ch_recommend_request.basic_consume(cb_recommend_request,
                                           queue=queue_name,
                                           no_ack=True)

        ch_db_changed = mq.channel()
        ch_db_changed.exchange_declare(exchange=ex_db_changed,
                                       exchange_type='topic')
        result = ch_db_changed.queue_declare(exclusive=True)
        queue_name = result.method.queue
        ch_db_changed.queue_bind(exchange=ex_db_changed,
                                 queue=queue_name,
                                 routing_key=bk_db_changed)
        ch_db_changed.basic_consume(cb_db_changed,
                                    queue=queue_name,
                                    no_ack=True)
    except KeyboardInterrupt as e:
        mq.close()
        logging.error(e)
    except Exception as e:
        logging.error(e)


def main():
    global mq, ch_recommend_request, ch_db_changed

    try:
        init_mq()
        # logging.info("Init completed.")
        print(' [*] Waiting for logs. To exit press CTRL+C')
        ch_recommend_request.start_consuming()
        ch_db_changed.start_consuming()
    except KeyboardInterrupt:
        mq.close()


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


