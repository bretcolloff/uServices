#!/usr/bin/env python
import pika
from itertools import zip_longest
import json

inputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
outputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
input = inputconnection.channel()
output = outputconnection.channel()

print("starting")
input.queue_declare(queue='pageQueue')
output.queue_declare(queue='wordQueue')

def callback(ch, method, properties, body):
    # Body will be json, contains: text, title, number
    message = body.decode('UTF-8')
    parsedMessage = json.loads(message)

    title = parsedMessage["title"]
    pageNumber = parsedMessage["number"]
    words = parsedMessage["text"].split(" ")

    # The first word on the page should be =
    # ((pagenumber - 1)* page size) + 1
    wordIndex = ((pageNumber - 1) * 325) + 1

    for word in words:
        wordMessage = {}
        wordMessage["title"] = title
        wordMessage["pageNumber"] = pageNumber
        wordMessage["word"] = word
        wordMessage["wordIndex"] = wordIndex
        print(wordMessage)
        output.basic_publish(exchange='', routing_key='wordQueue', body=json.dumps(wordMessage))
        wordIndex +=1

input.basic_consume(callback,
                      queue='pageQueue',
                      no_ack=True)

input.start_consuming()
