import unittest
import sqlite3
from zoo_file_adapter import ZooFileAdapter
from zoo import Zoo
from subprocess import call


class ZooFileAdapterTest(unittest.TestCase):
    def setUp(self):
        call('py create_animals_database.py', shell=True)
        self.db_conn = sqlite3.connect('animals.db')

    def test_save_withou_existing_table(self):
        zoo = Zoo(self.db_conn, 10, 10000)
        zoo_adapter = ZooFileAdapter(self.db_conn, zoo)
        zoo_adapter.save()

        self.assertEqual(1, zoo.get_id())

    def test_save_zoo_with_animals(self):
        zoo = Zoo(self.db_conn, 10, 10000)
        zoo.accomodate_animal('tiger', 'pe6o', 10, 'male')
        zoo_adapter = ZooFileAdapter(self.db_conn, zoo)
        zoo_adapter.save()

        self.assertEqual(1, zoo_adapter.zoo.get_id())

        expected = ['pe6o : tiger, 10, 120.0']
        self.assertEqual(expected, zoo.see_animals())

    def tearDown(self):
        self.db_conn.commit()
        self.db_conn.close()
        call('rm -f animals.db', shell=True)

if __name__ == '__main__':
    unittest.main()
