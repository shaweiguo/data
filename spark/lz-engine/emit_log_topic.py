#!/usr/bin/env python
import pika
import sys

exchange_name = 'sanguo_topic'
credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('us', 5672, '/', credentials)

mq = pika.BlockingConnection(params)
channel = mq.channel()

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange=exchange_name,
                      routing_key=routing_key,
                      body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
mq.close()
