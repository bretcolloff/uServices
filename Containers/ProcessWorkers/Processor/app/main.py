#!/usr/bin/env python
import json
import pika

# Start 2 RabbitMQ connections, as we want to both send and recieve.
inputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
outputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
input = inputconnection.channel()
output = outputconnection.channel()

# Use 'pageQueue' and 'wordQueue' for input and output respectively.
input.queue_declare(queue='pageQueue')
output.queue_declare(queue='wordQueue')

# Process page messages into the word queue.
def callback(ch, method, properties, body):
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
        output.basic_publish(exchange='', routing_key='wordQueue', body=json.dumps(wordMessage))
        wordIndex +=1

input.basic_consume(callback,
                      queue='pageQueue',
                      no_ack=True)

input.start_consuming()
