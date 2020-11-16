from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class PingPong(Resource):

    def get(self):
        return 'pong'

api.add_resource(PingPong, '/ping')

if __name__ == '__main__':
    app.run(port='8000')