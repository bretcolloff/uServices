from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import os.path
import pika
import socket

app = Flask(__name__)
api = Api(app)

# Create the parser to get the requried details from the POST body.
parser = reqparse.RequestParser()
parser.add_argument('text')
parser.add_argument('title')

# Connect to RabbitMQ.
connection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
channel = connection.channel()

# Use the inputQuete queue.
channel.queue_declare(queue='inputQueue')

# Upon recieving correctly formed JSON, process it and add it to the queue.
class ReadWorker(Resource):
    def get(self):
        return "Please post data in the form {'input':'<data>'}"
    def post(self):
        args = parser.parse_args()
        text = str(args['text'])
        title = str(args['title'])

        # Form the message JSON.
        message = {}
        message["title"] = title
        message["text"] = text

        # Send the message.
        channel.basic_publish(exchange='',
                              routing_key='inputQueue',
                              body=json.dumps(message))
        return {'Status':'Uploaded', 'InputData': json.dumps(message)}, 201

api.add_resource(ReadWorker, '/')

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=80)
