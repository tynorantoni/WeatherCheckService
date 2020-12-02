from flask_restful import Resource


# class for health check service
class PingPong(Resource):

    def get(self):
        return 'pong'
