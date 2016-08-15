from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class WriteWorker(Resource):
    def get(self):
        return {'get': 'test'}

api.add_resource(WriteWorker, '/')

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=80)