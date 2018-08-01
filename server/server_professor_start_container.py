#!/usr/bin/env python

import pika
import json
from functions import start_container

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_start_container')


def start_container_2(name_container):
    response = start_container(name_container)
    return response


def on_request(ch, method, props, body):
    name_container = body.decode('utf-8')
    response = start_container_2(name_container)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)



channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_start_container')

print(" [x] server_professor_start_container")
channel.start_consuming()
