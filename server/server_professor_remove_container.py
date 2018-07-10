#!/usr/bin/env python

import pika
import json
from functions import remove_container

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_remove_container')


def remove_container_2(name_container):
    response = remove_container(name_container)
    return response


def on_request(ch, method, props, body):
    name_container = body.decode('utf-8')
    response = remove_container_2(name_container)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)



channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_remove_container')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
