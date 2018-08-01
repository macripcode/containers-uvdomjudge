#!/usr/bin/env python
import pika
import json
from functions import enroll_course

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue_enroll_student')


def enroll_student(data):
    print("dato del estudiante")
    print(type(data))
    print(data)
    response = enroll_course(data)
    return response


def on_request(ch, method, props, body):
    data = json.loads(body.decode('utf-8'))
    response = enroll_student(data)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='queue_enroll_student')

print(" [x] server_enroll_student")
channel.start_consuming()
