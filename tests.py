import unittest


from flask import  Flask

from dbconnector import connect_to_db


class MyTestCase(unittest.TestCase):

    def test_connect_to_db(self):
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        self.assertIsNotNone(db_version, "connected")

    def test_get_json_from_api(self):
        self.assertEqual(True, False)

    def test_write_to_db(self):
        self.assertEqual(True,False)

    def test_cronjob(self):
        self.assertEqual(True, False)

    def test_pong(self):

        test_app = Flask(__name__)
        with test_app.test_client() as t:
            value = t.get('/ping')
        self.assertEqual(value,'pong')



if __name__ == '__main__':
    unittest.main()

