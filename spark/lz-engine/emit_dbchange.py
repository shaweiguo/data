#!/usr/bin/env python
import pika
import sys
import json

# mq = None
# ch_recommend_request = None
# ch_db_changed = None
# ex_recommend_request = 'sflz.ex.intelligent.recommend'
# bk_recommend_request = "sflz.rk.intelligent.recommend"
ex_db_changed = 'sflz.ex.changedb'
rk_db_changed = "sflz.rk.changedb.notification"

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('us', 5672, '/', credentials)

mq = pika.BlockingConnection(params)
ch_db_changed = mq.channel()

ch_db_changed.exchange_declare(exchange=ex_db_changed, exchange_type='topic')

# rk_db_changed = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or """
{"operation": "create | update | delete", "db_name": "yb", "collection": "AppConfig", "data": [{"id": "5c2b1ec77a8922c6997961d1"}]}
"""
ch_db_changed.basic_publish(exchange=ex_db_changed, routing_key=rk_db_changed, body=message)
print(" [x] Sent %r:%r" % (rk_db_changed, message))
mq.close()


msg = """
{"operation": "create | update | delete", "db_name": "yb", "collection": "AppConfig", "data": [{"id": "5c2b1ec77a8922c6997961d1"}]}
"""


def str2obj(s):
    obj = json.loads(s)
    print(obj)
    print(obj['collection'])


str2obj(msg)
#
# def obj2str(obj):
#     s = json.dumps(obj)
#     print(s)
#
#
# o = {
#     "operation":"create | update | delete",
#     "db_name": "yb",
#     "collection": "AppConfig",
#     "data": [
#         {
#             "id": "5c2b1ec77a8922c6997961d1"
#         }
#     ]
# }
#
# print(o)
# obj2str(o)
