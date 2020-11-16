import requests

from dbconnector import connect_to_db


def create_table():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE brussels_data
    (id SERIAL PRIMARY KEY NOT NULL,
    date_of_count DATE,
    hour_cnt VarChar(5),
    day_cnt VarChar(10),
    year_cnt VarChar(15),
    cnt_time TIMESTAMP);''')

    conn.commit()
    cur.close()
    conn.close()

def list_of_all_counters():
    device_url = 'https://data.mobility.brussels/bike/api/counts/?request=devices'
    device_req = requests.get(device_url)
    json = device_req.json()
    count = 0
    device_dict= {}
    for j in json['features']:
        road_name = json['features'][count]['properties']['road_en']
        device_id = json['features'][count]['properties']['device_name']
        device_dict[road_name] = device_id
        count += 1
    return device_dict

def insert_all_data():

    url='https://data.mobility.brussels/bike/api/counts/' \
        '?request=history&featureID={}&startDate=20201115&endDate=20201115&outputFormat=json'.format(id)
    request = requests.get(url)
    json = request.json()
    total=0
    for j in json['data']:
        total+=j['count']
        print(total)
    # print(json['data'][0])