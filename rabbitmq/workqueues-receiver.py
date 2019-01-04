#!/usr/bin/env python
import pika
import time

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

queue_name = 'task_queue'

channel.queue_declare(queue=queue_name, durable=True)


def callback(ch, method, properties, body):
    print(' [x] Received {}'.format(body))
    time.sleep(body.count(b'.'))
    print(' [x] Done')
    # ch.basic_ack(delivery_tag=method.delivery_tag)


# channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
