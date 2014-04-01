import sqlite3
import unittest
from subprocess import call
from animals import Animal

class TestAnimal(unittest.TestCase):
    """docstring for TestAnimal"""
    def setUp(self):
        call("py create_animals_database.py",shell=True)
        self.db_conn = sqlite3.connect("animals.db")

    def test_grow_young_animal(self):
        self.animal = Animal(self.db_conn, "tiger", 12, "Pol", "male", 30)
        self.animal.grow()
        self.assertEqual(13, self.animal.age)
        self.assertEqual(42, self.animal.weight)

    def test_grow_old_animal(self):
        self.animal = Animal(self.db_conn, "lion", 180, "John", "male", 201)
        self.animal.grow()
        self.assertEqual(201, self.animal.weight)
        self.assertEqual(181, self.animal.age)

    def test_die(self):
        self.animal = Animal(self.db_conn, "raccoon", 35, "Cohnen", "male", 60)
        self.assertEqual(True, self.animal.die())

    def tearDown(self):
    	call("rm animals.db",shell=True)

if __name__ == '__main__':
    unittest.main()