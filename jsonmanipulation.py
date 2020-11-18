import datetime

import requests
from requests import RequestException

from dbmanipulation import insert_to_db


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


def insert_all_data(start_date,end_date):
    # start_date = datetime.date(2018, 12, 5)
    # end_date = datetime.date(2020, 11, 17)
    delta = datetime.timedelta(days=1)
    devices = list_of_all_counters()
    while start_date <= end_date:
        for device in devices:
            json = get_json_from_location(devices[device], start_date, start_date)
            no_of_cyclists = count_all_the_cyclists(json)
            insert_to_db(start_date, device, no_of_cyclists)
        start_date += delta