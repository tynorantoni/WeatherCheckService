import psycopg2

from dbconnector import connect_to_db


def create_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute('''CREATE TABLE weather_data
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
        ice_prediction NUMERIC,
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


def insert_to_db(**kwargs):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute('''INSERT INTO weather_data (
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
                ice_chance
                ice_prediction,
                ) VALUES 
                ({},{},{},{},{},{},{},{},{},{},{},{},{},{});'''.format(
            kwargs
            )
                    )

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cur.close()
        conn.close()



