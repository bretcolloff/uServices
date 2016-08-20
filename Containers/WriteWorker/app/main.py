#!/usr/bin/env python
from elasticsearch import Elasticsearch
import json
import pika
import uuid

# Connect to ElasticSearch.
es = Elasticsearch([{'host': 'dockermachine', 'port': 9200}])

# Connect to RabbitMq.
inputconnection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))

# Use the 'wordQueue' queue.
input = inputconnection.channel()
input.queue_declare(queue='wordQueue')

# Transform the message from the queue and send the output to ElasticSearch.
def callback(ch, method, properties, body):
    # Turn the string into JSON.
    message = body.decode('UTF-8')
    parsedMessage = json.loads(message)

    # Take the details we want.
    title = parsedMessage["title"]
    word = parsedMessage["word"]
    wordIndex = parsedMessage["wordIndex"]
    pageNumber = parsedMessage["pageNumber"]
    docId = str(uuid.uuid4())

    # Write the document to elasticsearch.
    es.index(index="words", doc_type="word", id=docId, body={"title": title, "word": word, "pageNumber": pageNumber, "wordIndex": wordIndex})

input.basic_consume(callback,
                      queue='wordQueue',
                      no_ack=True)

# Start watching the queue.
input.start_consuming()
