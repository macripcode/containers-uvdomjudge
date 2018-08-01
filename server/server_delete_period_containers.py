#!/usr/bin/env python
# -*- coding: utf-8 -*-.
import pika
import requests
from functions import delete_containers_period


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_delete_period_containers')

def delete_period_containers(id_period):
    response = delete_containers_period(id_period)
    return response



def on_request(ch, method, props, body):
    id_period = body.decode('utf-8')
    response = delete_period_containers(id_period)
    print(response)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_delete_period_containers')

print(" [x] server_delete_period_containers")
channel.start_consuming()


