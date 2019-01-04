#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

queue_name = 'task_queue'

channel.queue_declare(queue=queue_name, durable=True)

msg = ' '.join(sys.argv[1:]) or 'Hello World!'

channel.basic_publish(exchange='', routing_key=queue_name, body=msg,
                      properties=pika.BasicProperties(delivery_mode=2,))
# channel.basic_publish(exchange='', routing_key=queue_name, body=msg)
print(' [x] Sent {}'.format(msg))

connection.close()
