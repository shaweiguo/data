#!/usr/bin/env python
import pika
import sys
import json

# mq = None
# ch_recommend_request = None
# ch_db_changed = None
ex_recommend_request = 'sflz.ex.intelligent.recommend'
rk_recommend_request = "sflz.rk.intelligent.recommend"

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('us', 5672, '/', credentials)

mq = pika.BlockingConnection(params)
ch_recommend_request = mq.channel()

ch_recommend_request.exchange_declare(exchange=ex_recommend_request, exchange_type='topic')

# rk_db_changed = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or """
{
    "user_id": "5c2b1ec77a8922c6997961d1",
    "prescription_id": "5bff959d5f627d6818eb28b7",
    "user_lat": 106.26,
    "user_lng": 38.447,
    "plan_num": 20
}
"""
ch_recommend_request.basic_publish(exchange=ex_recommend_request, routing_key=rk_recommend_request, body=message)
print(" [x] Sent %r:%r" % (rk_recommend_request, message))
mq.close()
