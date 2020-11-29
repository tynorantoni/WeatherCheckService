import datetime

import psycopg2
import pytest
import requests

from requests import RequestException

import pingpong
from dbconnector import connect_to_db
from weatherjsonparser import get_weather_json


class TestClass:

    @pytest.fixture()
    def setUp(self):
        connection = connect_to_db()
        yield connection
        connection.close()

    def test_connect_to_db(self, setUp):

        cur = setUp.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        assert db_version is not None

    def test_create_table(self, setUp):

        cur = setUp.cursor()

        cur.execute('''CREATE TABLE weather_data_test_table
                (id SERIAL PRIMARY KEY NOT NULL,
                day TIMESTAMP,
                temp NUMERIC,
                realfeel NUMERIC,
                dew_point NUMERIC,
                humidity NUMERIC,
                wind NUMERIC,
                wind_gust NUMERIC,
                wind_direction TEXT,
                rain_chance NUMERIC,
                rain_prediction NUMERIC,
                snow_chance NUMERIC,
                snow_prediction NUMERIC,
                ice_chance NUMERIC,
                ice_prediction NUMERIC
                );'''
                    )

        setUp.commit()
        query = cur.execute('SELECT * FROM weather_data_test_table;')
        assert query is None


    def test_insert_to_db(self, setUp):


        cur = setUp.cursor()

        cur.execute('''INSERT INTO weather_data_test_table (
                day,
                temp,
                realfeel,
                dew_point,
                humidity,
                wind,
                wind_gust,
                wind_direction,
                rain_chance,
                rain_prediction,
                snow_chance,
                snow_prediction,
                ice_chance,
                ice_prediction
                ) VALUES 
                ({},{},{},{},{},{},{},{},{},{},{},{},{},{});'''.format(
            day='2020-11-29T19:00:00+01:00',
            temp=-1.5,
            realfeel=-1.4,
            dew_point=-3.0,
            humidity=90,
            wind=5.6,
            wind_gust=9.3,
            wind_direction='NW',
            rain_chance=0,
            rain_prediction=0,
            snow_chance=13,
            snow_prediction=0,
            ice_chance=0,
            ice_prediction=0
        )
        )

        setUp.commit()

        query = cur.execute('SELECT ice_chance FROM weather_data_test_table;')
        print(query)
        assert query == 666




    def test_drop_table(self, setUp):
        with pytest.raises(psycopg2.DatabaseError):
            cur = setUp.cursor()

            cur.execute('''DROP TABLE weather_data_test_table;''')
            setUp.commit()
            cur.execute('SELECT * FROM weather_data_test_table;')

    def test_get_weather_json(self):
        try:
            url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' \
                  '274455?apikey=foWnaIP0eucDHJdMSpn2tAT6boAH4gkv&language=pl-PL&details=true&metric=true'

            request = requests.get(url)
            assert request.status_code == 200

        except RequestException as error:
            print(error)

    def test_insert_values_to_db(self):
        json = get_weather_json()
        assert len(json) == 12

    # @pytest.fixture()
    # def setUpFlask(self):
    #     pingpong.app.testing = True
    #
    #     with pingpong.app.test_client() as client:
    #         with pingpong.app.app_context():
    #             pingpong.start()
    #         yield client
    #
    # def test_pong(self,setUpFlask):
    #     value = setUpFlask.get('/ping')
    #     assert '200' in str(value)


if __name__ == '__main__':
    pytest.main()
