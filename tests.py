import unittest


class MyTestCase(unittest.TestCase):

    def test_connect_to_db(self):
        self.assertEqual(True, False)

    def test_get_json_from_api(self):
        self.assertEqual(True, False)

    def test_write_to_db(self):
        self.assertEqual(True,False)

    def test_cronjob(self):
        self.assertEqual(True, False)

    def test_pong(self):
        self.assertEqual(True, False)



if __name__ == '__main__':
    unittest.main()
