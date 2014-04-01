import sqlite3
from animals import Animal
from random import randint


class Zoo():
    """docstring for Zoo"""
    def __init__(self, db_conn, capacity, budget):
        self.__id = -1
        self.db_conn = db_conn
        self.capacity = capacity
        self.budget = budget
        self.animals = []

    def get_id(self):
        return self.__id

    def set_id(self, new_id):
        self.__id = new_id

    def accomodate_animal(self, species, name, age, gender):
        if len([a for a in self.animals if a.name == name and
            a.species == species]) != 0 or len(self.animals) >= self.capacity:
            return False

        self.animals.append(Animal(self.db_conn, species, age, name, gender))
        return True

    def move_to_habitat(self, species, name):
        old_count = len(self.animals)
        self.animals = [animal for animal in self.animals
                if animal.species != species and animal.name != name]
        if old_count > len(self.animals):
            return True
        return False

    def see_animals(self):
        return ['{0} : {1}, {2}, {3}'.format(animal.name, animal.species,
            animal.age, animal.weight) for animal in self.animals]

    def _mate_animals(self, current_month):
        females = [animal for animal in self.animals\
                if animal.gender == 'female']
        males = [animal for animal in self.animals if animal.gender == 'male']

        for female in females:
            num_males = len([m for m in males if m.species == female.species])
            is_time = (current_month % (6 + female.get_gestation_period())) == 0

            if num_males != 0 and is_time:
                gender = 'male'
                if randint(0, 100) < 50:
                    gender = 'female'
                self.animals.append(Animal(self.db_conn, female.species, 0,
                    'Bebe', gender))

    def simulate(self, interval, period):
        pass

    def income(self):
        return len(self.animals) * 60

    def get_budget(self):
        return self.budget

    def expenses(self):
        all_exp = 0
        for animal in self.animals:
            all_exp += animal.expenses_for_food()
        return all_exp
