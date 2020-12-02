import psycopg2

from dbconnector import connect_to_db


# basic DB manipulation functions

def create_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute('''CREATE TABLE weather_data
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

        cur.execute('''DROP TABLE weather_data;''')
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cur.close()
        conn.close()


def insert_to_db(connection, **kwargs):
    try:
        cur = connection.cursor()

        cur.execute('''INSERT INTO weather_data (
        date_of_measure, temperature, realfeel, dew_point, humidity, wind, wind_gust, wind_direction,
        rain_chance, rain_prediction, snow_chance, snow_prediction, ice_chance, ice_prediction
                ) VALUES ('{}',{},{},{},{},{},{},'{}',{},{},{},{},{},{});'''.format(
            kwargs['date_of_measure'],
            kwargs['temperature'],
            kwargs['realfeel'],
            kwargs['dew_point'],
            kwargs['humidity'],
            kwargs['wind'],
            kwargs['wind_gust'],
            kwargs['wind_direction'],
            kwargs['rain_chance'],
            kwargs['rain_prediction'],
            kwargs['snow_chance'],
            kwargs['snow_prediction'],
            kwargs['ice_chance'],
            kwargs['ice_prediction']
        ))

        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
