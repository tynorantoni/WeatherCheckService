import datetime

import psycopg2
import requests
from requests import RequestException

from dbconnector import connect_to_db


def create_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute('''CREATE TABLE brussels_data
        (id SERIAL PRIMARY KEY NOT NULL,
        date_of_count DATE,
        street_name TEXT,
        day_cnt VarChar(10));'''
                    )

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cur.close()
        conn.close()


def drop_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute('''DROP TABLE brussels_data;''')
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cur.close()
        conn.close()


def insert_to_db(date_of_counting, street_name, total_cyclists):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute('''INSERT INTO brussels_data 
        (date_of_count, street_name, day_cnt) VALUES 
        ({},{},{});'''.format(date_of_counting, street_name, total_cyclists)
                    )

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cur.close()
        conn.close()


def list_of_all_counters():
    try:
        device_url = 'https://data.mobility.brussels/bike/api/counts/?request=devices'
        device_req = requests.get(device_url)
        json = device_req.json()
        count = 0
        device_dict = {}
        for j in json['features']:
            road_name = json['features'][count]['properties']['road_en']
            device_id = json['features'][count]['properties']['device_name']
            device_dict[road_name] = device_id
            count += 1
        return device_dict
    except RequestException as error:
        print(error)


def get_json_from_location(device_id, start_date, end_date):
    try:
        url = 'https://data.mobility.brussels/bike/api/counts/' \
              '?request=history&featureID={}&startDate={}&endDate={}&outputFormat=json' \
            .format(device_id, start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"))

        request = requests.get(url)
        json = request.json()
        return json
    except RequestException as error:
        print(error)


def count_all_the_cyclists(json):
    try:
        total_value = 0
        for j in json['data']:
            total_value += j['count']

        return total_value
    except Exception as error:
        print(error)


def insert_all_data():
    start_date = datetime.date(2019, 12, 24)
    end_date = datetime.date(2019, 12, 25)
    delta = datetime.timedelta(days=1)
    devices = list_of_all_counters()
    while start_date <= end_date:
        for device in devices:
            json = get_json_from_location(devices[device], start_date, start_date)
            no_of_cyclists = count_all_the_cyclists(json)
            insert_to_db(start_date, device, no_of_cyclists)
        start_date += delta
