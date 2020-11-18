import datetime

from jsonmanipulation import insert_all_data
from pingpong import start


def get_json_from_api():
    yesterday = datetime.today() - datetime.timedelta(days=1)
    insert_all_data(yesterday,yesterday)




if __name__ == '__main__':

    # get_json_from_api()
    start()

