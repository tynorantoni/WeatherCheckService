from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
# app.testing= True

class PingPong(Resource):
    def get(self):
        return 'pong'

def start():
    api.add_resource(PingPong, '/ping')
    app.run(port='8000')