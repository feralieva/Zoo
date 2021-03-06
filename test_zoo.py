import unittest
import sqlite3
from zoo import Zoo
from animals import Animal
from subprocess import call


class ZooTest(unittest.TestCase):
    def setUp(self):
        call('py create_animals_database.py', shell=True)
        self.db_conn = sqlite3.connect('animals.db')
        self.zoo = Zoo(self.db_conn, 2, 1000)
        self.zoo.animals = [Animal(self.db_conn, 'lion', 9, 'luv4o', 'male')]

    def test_see_animals(self):
        expected = ['luv4o : lion, 9, 67.5']
        self.assertEqual(expected, self.zoo.see_animals())

    def test_see_no_animals(self):
        self.zoo.animals = []
        self.assertEqual([], self.zoo.see_animals())

    def test_accomodate_animal(self):
        self.zoo.accomodate_animal('tiger', 'pe6o', 10, 'male')
        expected = ['luv4o : lion, 9, 67.5',
                    'pe6o : tiger, 10, 120.0']
        self.assertEqual(expected, self.zoo.see_animals())

    def test_accomodate_over_capacity(self):
        self.zoo.accomodate_animal('tiger', 'pe6o', 10, 'male')
        res = self.zoo.accomodate_animal('tiger', 'pe6ovica', 10, 'female')
        self.assertFalse(res)

        expected = ['luv4o : lion, 9, 67.5',
                    'pe6o : tiger, 10, 120.0']
        self.assertEqual(expected, self.zoo.see_animals())

    def test_move_to_habitat(self):
        result = self.zoo.move_to_habitat('lion', 'luv4o')
        expected = []
        self.assertTrue(result)
        self.assertEqual(expected, self.zoo.see_animals())

    def test_move_to_haibtat_with_non_existing_animal(self):
        result = self.zoo.move_to_habitat('asd', 'asd')
        self.assertFalse(result)

    def test_mate_animals(self):
        self.zoo.accomodate_animal('lion', 'pe6a', 10, 'female')
        self.zoo._mate_animals(9)
        self.assertEqual(3, len(self.zoo.animals))

    def test_simulate(self):
        self.zoo.animals = [Animal(self.db_conn, 'lion', 1, 'luv4o', 'male')]
        expected = ['month 1:',
                    'luv4o : lion, 2, 15.0',
                    'No animals have died during the past month.',
                    'No animals were born during the past month.',
                    'The current budget is 1057.92']
        self.assertEqual(expected, self.zoo.simulate('months', 1))

    def tearDown(self):
        self.db_conn.commit()
        self.db_conn.close()
        call('rm -f animals.db', shell=True)

if __name__ == '__main__':
    unittest.main()
