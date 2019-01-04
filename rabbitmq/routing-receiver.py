#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

exchange_name = 'direct_logs'

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write('Usage: {} [info] [warning] [error]\n'.format((sys.argv[0])))
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=severity)

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(' [x] Received {}:{}'.format(method.routing_key, body))


# channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
