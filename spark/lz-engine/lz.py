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

table_names = ['SFLZ_AppConfig', 'XHHK_Application', 'SFLZ_APPMedicine',
               'SFLZ_Medicine', 'SFLZ_Prescription', 'SFLZ_StdMedicine']
_rdds = {}


def get_rdd(table_name):
    uri = "mongodb://root:q1w2e3r4@us:27017/yb"
    uri = uri + ".{}?authSource=admin&readPreference=primaryPreferred".format(table_name)
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
        .option("uri", uri)\
        .load()
    df.cache()
    df.createOrReplaceTempView(table_name)

    return df


def init_rdds():
    global _rdds, table_names

    for table_name in table_names:
        _rdds[table_name] = None

    # table_names = ['AppConfig', 'Application', 'APPMedicine', 'Medicine', 'Prescription', 'StdMedicine']
    for table_name in table_names:
        _rdds[table_name] = get_rdd(table_name)

    for table_name in table_names:
        _rdds[table_name].show(20)


def update_rdd(table_name):
    global _rdds
    _rdds[table_name] = get_rdd(table_name)
    _rdds[table_name].show()


def cb_recommend_request(ch, method, properties, body):
    # logging.info(" [x] %r " % body)
    print(" [x] %r " % body)
    rec_req = json.loads(body.decode('utf-8'))

    recommend_apps = []
    try:
        # first step:
        prescription_id = rec_req['prescription_id']
        print('prescription_id: {}'.format(prescription_id))
        # app_id = _rdds['Prescription'].filter('_id = {}'.format(prescription_id)).first()['hosp_id']
        # _rdds['Prescription'].show()
        # _rdds['Prescription'].filter('_id = {}'.format(prescription_id)).show()
        app_id = _rdds['SFLZ_Prescription'].filter(_rdds['SFLZ_Prescription']._id == prescription_id).first()['hosp_id']
        print('-------------------------------------------------------------------------------------')
        print('app_id: {}'.format(app_id))
        print('-------------------------------------------------------------------------------------')

        # second step:
        apps = [app_id]
        sql = "select app_id from SFLZ_AppConfig where collaborate_type <> 1"
        ids = spark.sql(sql).collect()
        appids = [row.app_id for row in ids]
        apps.extend(appids)
        # apps.append(app_id)
        print(apps)

        # Third step
        print('333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333')
        # sql = """SELECT A.app_id, A.std_medicine_id, A.medicine_name, A.price, A.num AS stock,
        #             B.ord_qty, A.price * B.ord_qty AS sum_price, A.manufacture FROM SFLZ_AppMedicine as A
        #             LEFT JOIN SFLZ_Medicine as B
        #             ON (A.std_medicine_id = B.std_medicine_id)
        #             WHERE A.obsoleted = 'False'
        #                 AND A.std_medicine_id IN (
        #                     SELECT std_medicine_id FROM SFLZ_Medicine WHERE prescription_id = '{}'
        #                 )
        #                 AND A.app_id IN (
        #                     SELECT app_id FROM SFLZ_AppConfig WHERE collaborate_type <> 1
        #                 )
        #         """.format(prescription_id)
        sql = "select std_medicine_id, ord_qty from SFLZ_Medicine where prescription_id = '{}'".format(prescription_id)
        print(sql)
        medicines = spark.sql(sql).collect()
        print(medicines)

        # Fourth step
        print('444444444444444444444444444444444444444444444444444444444444444444444444444444444444444')
        sql = """SELECT app_id, std_medicine_id, medicine_name, price, num, manufacture, obsoleted
                    FROM SFLZ_AppMedicine
                    WHERE obsoleted = 'False'
                        AND std_medicine_id IN (
                            SELECT std_medicine_id FROM SFLZ_Medicine WHERE prescription_id = '{}'
                        )
                        AND app_id IN (
                            SELECT app_id FROM SFLZ_AppConfig WHERE collaborate_type <> 1
                        )
                """.format(prescription_id)
        app_medicines = spark.sql(sql).collect()
        print(app_medicines)
        # m_apps = {}
        # for medicine in medicines:
        #     print(medicine)
        #     m_apps[medicine.std_medicine_id] = []
        #     sql = "select app_id from SFLZ_AppMedicine where std_medicine_id='{}' and num>={}".format(
        #         medicine.std_medicine_id, medicine.ord_qty)
        #     print(sql)
        #     count = spark.sql(sql).count()
        #     if count > 0:
        #         app_ids = spark.sql(sql).collect()
        #         m_apps[medicine.std_medicine_id].extend([row.app_id for row in app_ids])
        #     else:
        #         break
        # print(m_apps)
        # all_apps = set()
        # for k in m_apps.keys():
        #     for v in m_apps[k]:
        #         all_apps.add(v)
        # apps = set()
        # count = len(m_apps.keys())
        # for app in all_apps:
        #     for k in m_apps.keys():
        #         for v in m_apps[k]:
        #             if v == app:
        #                 count = count - 1
        #     if count > 0:
        #         apps.add(app)
        # ids = ''
        # for app in apps:
        #     ids.join("'{}',".format(app))
        # if len(ids) > 1:
        #     ids = ids[:-2]
        # sql = "select * from SFLZ_AppMedicine where app_id in ({})".format(ids)
        # p_apps = spark.sql(sql).groupBy('app_id').sum()
    except Exception as ex:
        print(ex)


def cb_db_changed(ch, method, properties, body):
    # logging.info(" [x] %r " % body)
    print(" [x] %r:%r" % (method.routing_key, body))
    # msg = body.decode('utf-8')
    # print(msg)
    db_changed = json.loads(body.decode('utf-8'))
    print(db_changed)
    # print(db_changed.keys())
    # print(db_changed.values())
    table_name = db_changed['collection']
    update_rdd(table_name)


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
        init_rdds()
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
