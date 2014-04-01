import unittest
import sqlite3
from zoo_file_adapter import ZooFileAdapter
from zoo import Zoo
from subprocess import call


class ZooFileAdapterTest(unittest.TestCase):
    def setUp(self):
        self.db_conn = sqlite3.connect('zoos.db')

    def test_save_withou_existing_table(self):
        zoo = Zoo(self.db_conn, 10, 10000)
        zoo_adapter = ZooFileAdapter(self.db_conn, zoo)
        zoo_adapter.save()

        self.assertEqual(1, zoo.get_id())

    def tearDown(self):
        call('rm -f zoos.db', shell=True)

if __name__ == '__main__':
    unittest.main()
