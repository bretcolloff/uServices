#!/usr/bin/env python
from itertools import zip_longest
import json
import pika

# Start 2 RabbitMQ connections, as we want to both send and recieve.
inputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
outputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
input = inputconnection.channel()
output = outputconnection.channel()

# use 'inputQueue' and 'pageQueue' for input and output respectively.
input.queue_declare(queue='inputQueue')
output.queue_declare(queue='pageQueue')

# Group a list into lists of size n.
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=" ")

# Process messages from the input queue.
def callback(ch, method, properties, body):
    # Split the text into words.
    message = body.decode('UTF-8')
    parsedMessage = json.loads(message)
    words = parsedMessage["text"].split(" ")
    title = parsedMessage["title"]

    # Group the words into pages.
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
