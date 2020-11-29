from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api
from pingpong import PingPong
import datetime

from weatherjsonparser import insert_all_data


class Config(object):
    JOBS = [
        {
            'id': 'check_weather',
            'func': 'app:check_weather',
            'trigger': 'interval',
            'seconds': 1800
        }
    ]

    SCHEDULER_API_ENABLED = True


def check_weather():

    pass




app = Flask(__name__)
app.config.from_object(Config())
api = Api(app)
api.add_resource(PingPong, '/ping')
scheduler = APScheduler()
# it is also possible to enable the API directly
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()
if __name__ == '__main__':
    app.run(host='0.0.0.0')

