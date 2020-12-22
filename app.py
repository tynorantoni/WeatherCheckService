from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api
from pingpong import PingPong

from weatherjsonparser import insert_values_to_db, get_weather_json


# config scheduling class
class Config(object):
    JOBS = [
        {
            'id': 'check_weather',
            'func': 'app:check_weather',
            'trigger': 'interval',
            'seconds': 10800
        }
    ]

    SCHEDULER_API_ENABLED = True


# function triggered every 3 hours
def check_weather():
    insert_values_to_db(get_weather_json())


# flask startup
app = Flask(__name__)
app.config.from_object(Config())

api = Api(app)
api.add_resource(PingPong, '/ping')  # add resource URL

# initiate scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
