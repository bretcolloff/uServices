from flask import Flask
from flask_restful import Resource, Api, reqparse
import pika
import os.path
import socket

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('input')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='dockermachine'))
channel = connection.channel()

channel.queue_declare(queue='inputQueue')

class ReadWorker(Resource):
    def get(self):
        return "Please post data in the form {'input':'<data>'}"
    def post(self):
        args = parser.parse_args()
        bodyText = str(args['input'])
        channel.basic_publish(exchange='',
                              routing_key='inputQueue',
                              body=bodyText)
        return {'Status':'Uploaded', 'InputData': bodyText}, 201

api.add_resource(ReadWorker, '/')

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=80)
