import unittest, sqlite3
from animals import Animal
from animals_file_adapter import AnimalFileAdapter
from subprocess import call


class AnimalFileAdapterTest(unittest.TestCase):
    """docstring for AnimalFileAdapterTest"""
    def setUp(self):
        call("py create_animals_database.py",shell=True)
        self.db_conn = sqlite3.connect("animals.db")
        self.animal = Animal(self.db_conn, "tiger", 12, "Pol", "male")

        self.animals_adapter = AnimalFileAdapter(self.db_conn, self.animal)

    def test_prepare_to_save(self):
        expected = ('Pol', 'tiger', 12, 'male', 144.0)
        self.assertEqual(expected, self.animals_adapter.prepare_to_save())

    def test_save_new_animal(self):
        self.animals_adapter.save()
        self.assertEqual(1, self.animal.get_id())

    def test_save_update_animal(self):
        self.animals_adapter.save()
        self.animal.age = 13
        self.animals_adapter.save()

        sql = 'select age from zoo_animals where id=?'
        cursor = self.db_conn.cursor()
        actual = cursor.execute(sql, (self.animal.get_id(), )).fetchone()[0]

        self.assertEqual(13, actual)

    def test_load(self):
        self.animals_adapter.save()
        file_adapter = AnimalFileAdapter(self.db_conn, Animal(self.db_conn,
            'lion', 1, '', ''))
        self.assertTrue(file_adapter.load(1))
        expected = ('Pol', 'tiger', 12, 'male', 144.0)
        self.assertEqual(expected, file_adapter.prepare_to_save())

    def tearDown(self):
        self.db_conn.commit()
        self.db_conn.close()
        call('rm -f animals.db', shell=True)

if __name__ == '__main__':
    unittest.main()
