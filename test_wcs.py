import psycopg2
import pytest
import requests

from requests import RequestException

import pingpong
from dbconnector import connect_to_db
from weatherjsonparser import get_weather_json


class TestClass:

    # setup db connection
    @pytest.fixture()
    def setUp(self):
        connection = connect_to_db()
        yield connection
        connection.close()

    # connect to DB
    def test_connect_to_db(self, setUp):

        cur = setUp.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        assert db_version is not None

    # create table for testing
    def test_create_table(self, setUp):

        cur = setUp.cursor()

        cur.execute('''CREATE TABLE weather_data_test_table
                (id SERIAL PRIMARY KEY NOT NULL,
                date_of_measure TIMESTAMP,
                temperature NUMERIC,
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
        cur.execute('SELECT * FROM weather_data_test_table;')
        assert cur.fetchone() is None

    # insert mocked data to DB
    def test_insert_to_db(self, setUp):

        cur = setUp.cursor()

        cur.execute('''INSERT INTO weather_data_test_table (
                date_of_measure,
                temperature,
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
                ) VALUES (
					'2020-05-28 19:00:00', -1.5,-1.4,
            -3.0,
            90,
            5.6,
            9.3,
            'NW',
            0,
            0,
            13,
            0,
            666,
            0		
        );''')

        rows = cur.rowcount
        setUp.commit()
        assert 1 == rows

    # drop test table after tests
    def test_drop_table(self, setUp):
        try:
            cur = setUp.cursor()

            cur.execute('''DROP TABLE weather_data_test_table;''')
            setUp.commit()
            assert cur.statusmessage == 'DROP TABLE'
        except psycopg2.DatabaseError as error:
            print(error)

    # testing Accuweather API
    def test_get_weather_json(self):
        try:
            url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' \
                  '274455?apikey=foWnaIP0eucDHJdMSpn2tAT6boAH4gkv&language=pl-PL&details=true&metric=true'

            request = requests.get(url)
            assert request.status_code == 200

        except RequestException as error:
            print(error)

    # test if json returns data for 12 hours
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
