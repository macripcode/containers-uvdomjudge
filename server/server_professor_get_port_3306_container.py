#!/usr/bin/env python

import pika
import json
from functions import get_port_3306

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_get_port_3306_container')


def get_port_3306_2(name_container):
    response = get_port_3306(name_container)
    return response


def on_request(ch, method, props, body):
    name_container = body.decode('utf-8')
    response = get_port_3306_2(name_container)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)



channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_get_port_3306_container')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
