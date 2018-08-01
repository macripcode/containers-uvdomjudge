#!/usr/bin/env python

import pika
import json
from functions import set_pass_admin_container

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_set_admin_container')


def set_pass_professor(data):
    print("el lazo 5")
    response = set_pass_admin_container(data)
    print("response del server set pass container")
    print(response)
    return response


def on_request(ch, method, props, body):
    data = json.loads(body.decode('utf-8'))
    print("data")
    print(data)
    print("el lazo 4")
    response = set_pass_professor(data)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_set_admin_container')

print(" [x] server_set_pass_container")
channel.start_consuming()
