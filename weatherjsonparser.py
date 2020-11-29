
import requests
from requests import RequestException

from dbmanipulation import insert_to_db



def get_weather_json():
    try:
        
        url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' \
              '274455?apikey=foWnaIP0eucDHJdMSpn2tAT6boAH4gkv&language=pl-PL&details=true&metric=true'

        request = requests.get(url)
        json = request.json()

        return json
    except RequestException as error:
        print(error)




def insert_values_to_db(json):
    try:
        for j in json:
            insert_to_db(
                day=j['DateTime'],
                temp=j['Temperature']['Value'],
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
    except(Exception) as error:
        print(error)


insert_values_to_db('json')