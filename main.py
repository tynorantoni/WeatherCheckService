import requests

from pingpong import start


def get_json_from_api():
    #get location of counters
    url = 'https://data.mobility.brussels/bike/api/counts/?request=devices'
    request = requests.get(url)
    json = request.json()
    count = 0
    for j in json['features']:
        print(json['features'][count]['properties']['road_en'])
        print(json['features'][count]['id'])
        count+=1

    #test of one device
    url_live = 'https://data.mobility.brussels/bike/api/counts/?request=live&featureID=CAT17'
    live_req= requests.get(url_live)
    json_live = live_req.json()
    print('live data ',json_live)





if __name__ == '__main__':
    get_json_from_api()
    start()

