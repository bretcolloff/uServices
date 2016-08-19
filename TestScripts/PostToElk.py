#!/usr/bin/env python
import pika
from itertools import zip_longest
import json
from elasticsearch import Elasticsearch

dockerHost = "10.82.53.41"

es = Elasticsearch([{'host': dockerHost, 'port': 9200}])

inputconnection = pika.BlockingConnection(pika.ConnectionParameters(host=dockerHost))
input = inputconnection.channel()

input.queue_declare(queue='wordQueue')

def callback(ch, method, properties, body):
    # Body will be json, contains: text, title, number
    message = body.decode('UTF-8')
    parsedMessage = json.loads(message)

    title = parsedMessage["title"]
    word = parsedMessage["word"]
    wordIndex = parsedMessage["wordIndex"]
    pageNumber = parsedMessage["pageNumber"]
    docId = title + str(pageNumber) + str(wordIndex) + word

    es.index(index="words", doc_type="word", id=docId, body={"title": title, "word": word, "pageNumber": pageNumber, "wordIndex": wordIndex})

input.basic_consume(callback,
                      queue='wordQueue',
                      no_ack=True)

input.start_consuming()
