#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

queue_name = 'hello'

channel.queue_declare(queue=queue_name)


def callback(ch, method, properties, body):
    print(' [x] Received {}'.format(body))


channel.basic_consume(callback, queue=queue_name, no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
