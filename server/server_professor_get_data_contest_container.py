#!/usr/bin/env python

import pika
import json
from functions import  get_data_contest_container

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_get_data_contest_container')


def get_data_contest_container2(name_container):
    response = get_data_contest_container(name_container)
    return response


def on_request(ch, method, props, body):
    name_container = body.decode('utf-8')
    response = get_data_contest_container2(name_container)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)



channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_get_data_contest_container')

print(" [x] server_professor_get_data_contest_container")
channel.start_consuming()
