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
                a.species == species]) != 0 or\
                len(self.animals) >= self.capacity:
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
        females = [animal for animal in self.animals
                   if animal.gender == 'female']
        males = [animal for animal in self.animals if animal.gender == 'male']

        newborns = []

        for female in females:
            num_males = len([m for m in males if m.species == female.species])
            is_time = (current_month % (6 + female.get_gestation_period()))\
                == 0

            if num_males != 0 and is_time:
                gender = 'male'
                if randint(0, 100) < 50:
                    gender = 'female'
                self.animals.append(Animal(self.db_conn, female.species, 0,
                                           'Bebe', gender))
                newborns.append('A little {} was born. It\'s name is {}'
                                .format(female.species, self.animals[-1].name))

        return newborns

    def simulate(self, interval, period):
        single_interval = 0
        if interval == 'months':
            single_interval = 1
        elif interval == 'years':
            single_interval = 12

        period_in_months = period * single_interval

        result = []
        while period_in_months > 0:
            dead_animals = []
            for animal in self.animals:
                animal.grow()
                if animal.die():
                    dead_animals.append('The {0} {1} have died during the '
                                        'past {2}'.format(animal.species,
                                                          animal.name,
                                                          interval[:-1]))
                    self.animals = [a for a in self.animals if not a == animal]

            self.budget -= self.expenses()
            self.budget += self.income()

            newborns = self._mate_animals(period * single_interval
                                          - period_in_months)

            if self.budget < 0:
                return 'No more money! The zoo is closing! X_X'

            period_in_months -= single_interval

            if period_in_months % single_interval == 0:
                current_period = period - period_in_months // single_interval
                result.append('{} {}:'.format(interval[:-1], current_period))
                result += self.see_animals()
                if len(dead_animals) > 0:
                    result += dead_animals
                else:
                    result.append('No animals have died during the past {}.'
                                  .format(interval[:-1]))

                if len(newborns) > 0:
                    result += newborns
                else:
                    result.append('No animals were born during the past {}.'
                                  .format(interval[:-1]))

                result.append('The current budget is {}'.format(self.budget))

        return result

    def income(self):
        return len(self.animals) * 60

    def get_budget(self):
        return self.budget

    def expenses(self):
        all_exp = 0
        for animal in self.animals:
            all_exp += animal.expenses_for_food()
        return all_exp
