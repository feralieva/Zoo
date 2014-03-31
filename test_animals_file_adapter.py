import unittest, sqlite3
from animals import Animal
from animals_file_adapter import AnimalFileAdapter
from subprocess import call


class AnimalFileAdapterTest(unittest.TestCase):
    """docstring for AnimalFileAdapterTest"""
    def setUp(self):
        call("py create_animals_database.py",shell=True)
        self.animals_db = sqlite3.connect("animals.db")
        self.animal = Animal(self.animals_db, "tiger", 12, "Pol", "male")

        self.zoo_db = sqlite3.connect('zoo.db')
        self.animals_adapter = AnimalFileAdapter(self.zoo_db, self.animal)

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

        sql = 'select age from animals where id=?'
        cursor = self.zoo_db.cursor()
        actual = cursor.execute(sql, (self.animal.get_id(), )).fetchone()[0]

        self.assertEqual(13, actual)

    def test_load(self):
        self.animals_adapter.save()
        file_adapter = AnimalFileAdapter(self.zoo_db, Animal(self.animals_db,
            'lion', 1, '', ''))
        self.assertTrue(file_adapter.load(1))
        expected = ('Pol', 'tiger', 12, 'male', 144.0)
        self.assertEqual(expected, file_adapter.prepare_to_save())

    def tearDown(self):
        self.animals_db.close()
        self.zoo_db.close()
        call('rm -f animals.db, zoo.db', shell=True)

if __name__ == '__main__':
    unittest.main()
