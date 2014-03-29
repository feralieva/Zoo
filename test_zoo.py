import unittest, sqlite3
from zoo import Zoo
from animals import Animal


class ZooTest(unittest.TestCase):
    def setUp(self):
        self.db_conn = sqlite3.connect('animals.db')
        self.zoo = Zoo(self.db_conn, 2, 1000)
        self.zoo.animals = [Animal(self.db_conn, 'lion', 9, 'luv4o', 'male',
            100)]

    def test_see_animals(self):
        expected = ['luv4o : lion, 9, 100']
        self.assertEqual(expected, self.zoo.see_animals())

    def test_see_no_animals(self):
        self.zoo.animals = []
        self.assertEqual([], self.zoo.see_animals())

    def test_accomodate_animal(self):
        self.zoo.accomodate_animal('bear', 'pe6o', 10, 100, 'male')
        expected = ['luv4o : lion, 9, 100',
                'pe6o : bear, 10, 100']
        self.assertEqual(expected, self.zoo.see_animals())

    def test_accomodate_over_capacity(self):
        self.zoo.accomodate_animal('bear', 'pe6o', 10, 100, 'male')
        res = self.zoo.accomodate_animal('bear', 'pe6ovica', 10, 100, 'female')
        self.assertFalse(res)

        expected = ['luv4o : lion, 9, 100',
                'pe6o : bear, 10, 100']
        self.assertEqual(expected, self.zoo.see_animals())

    def test_move_to_habitat(self):
        result = self.zoo.move_to_habitat('lion', 'luv4o')
        expected = []
        self.assertTrue(result)
        self.assertEqual(expected, self.zoo.see_animals())

    def test_simulate(self):
        pass

    def tearDown(self):
        self.db_conn.close()

if __name__ == '__main__':
    unittest.main()
