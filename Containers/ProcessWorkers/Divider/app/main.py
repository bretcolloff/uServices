#!/usr/bin/env python
import pika
from itertools import zip_longest
import json

inputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
outputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
input = inputconnection.channel()
output = outputconnection.channel()

input.queue_declare(queue='inputQueue')
output.queue_declare(queue='pageQueue')

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=" ")

def callback(ch, method, properties, body):
    # Split the book into words...
    message = body.decode('UTF-8')
    parsedMessage = json.loads(message)
    words = parsedMessage["text"].split(" ")
    title = parsedMessage["title"]
    # Split the book into pages...
    pages = grouper(words, 325)

    pagenumber = 1
    # Add each page to the queue
    for page in pages:
        pageMessage = {}
        pageMessage["title"] = title
        pageMessage["text"] = " ".join(page)
        pageMessage["number"] = pagenumber
        output.basic_publish(exchange='', routing_key='pageQueue', body=json.dumps(pageMessage))
        pagenumber += 1

input.basic_consume(callback,
                      queue='inputQueue',
                      no_ack=True)

input.start_consuming()
