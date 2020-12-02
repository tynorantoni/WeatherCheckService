import requests
from requests import RequestException

from dbconnector import connect_to_db
from dbmanipulation import insert_to_db


# get json from accuweather API (location - Krakow, 12hour prognosis)
def get_weather_json():
    try:

        url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' \
              '274455?apikey=foWnaIP0eucDHJdMSpn2tAT6boAH4gkv&language=pl-PL&details=true&metric=true'

        request = requests.get(url)
        json = request.json()
        print(json)
        return json
    except RequestException as error:
        print(error)




# insert values from json to DB
# accepts json with data for 12 hours, but inserts only first 3 hours.
def insert_values_to_db(json):
    try:
        conn = connect_to_db()
        for j in json[0:3]:
            insert_to_db(conn,
                         date_of_measure=j['DateTime'],
                         temperature=j['Temperature']['Value'],
                         realfeel=j['RealFeelTemperature']['Value'],
                         dew_point=j['DewPoint']['Value'],
                         humidity=j['RelativeHumidity'],
                         wind=j['Wind']['Speed']['Value'],
                         wind_gust=j['WindGust']['Speed']['Value'],
                         wind_direction=j['Wind']['Direction']['Localized'],
                         rain_chance=j['RainProbability'],
                         rain_prediction=j['Rain']['Value'],
                         snow_chance=j['SnowProbability'],
                         snow_prediction=j['Snow']['Value'],
                         ice_chance=j['IceProbability'],
                         ice_prediction=j['Ice']['Value']
                         )
        conn.close()
    except(Exception) as error:
        print(error)
