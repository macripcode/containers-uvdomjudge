#!/usr/bin/env python
import pika
import json
from functions import is_running_container

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_is_runing_container')


def is_running_container2(name_container):
    response = is_running_container(name_container)
    return response


def on_request(ch, method, props, body):
    print(body)
    name_container = body.decode('utf-8')
    response = is_running_container2(name_container)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_is_runing_container')

print(" [x] server_public_run_container")
channel.start_consuming()
