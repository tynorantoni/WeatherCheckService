from flask_restful import Resource


class PingPong(Resource):


    def get(self):
        return 'pong'
