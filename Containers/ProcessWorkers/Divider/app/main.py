#!/usr/bin/env python
import pika
from itertools import zip_longest

inputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
outputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
input = inputconnection.channel()
output = outputconnection.channel()

print("starting")
input.queue_declare(queue='inputQueue')
output.queue_declare(queue='pageQueue')

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=' ')

def callback(ch, method, properties, body):
    # Split the book into words...
    words = body.decode('UTF-8').split(" ")
    # Split the book into pages...
    pages = grouper(words, 325)

    # Add each page to the queue
    for page in pages:
        output.basic_publish(exchange='', routing_key='pageQueue', body=" ".join(page))

input.basic_consume(callback,
                      queue='inputQueue',
                      no_ack=True)

input.start_consuming()
