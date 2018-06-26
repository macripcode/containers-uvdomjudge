#!/usr/bin/env python
import pika
import json
from functions import run_container_course

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_run_container')


def run_container(container):
    print("dato de container")
    print(type(container))
    response = run_container_course(container)
    return response


def on_request(ch, method, props, body):
    print(body)
    container = json.loads(body.decode('utf-8'))
    response = run_container(container)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_run_container')

print(" [x] Awaiting RPC requests")
channel.start_consuming()

"""
from server import server_run_container

"""