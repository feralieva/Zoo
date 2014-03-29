from animals import Animal


class Zoo():
    """docstring for Zoo"""
    def __init__(self, db_conn, capacity, budget):
        self.db_conn = db_conn
        self.capacity = capacity
        self.budget = budget
        self.animals = []

    def accomodate_animal(self, species, name, age, weight, gender):
        if len([a for a in self.animals if a.name == name and
            a.species == species]) != 0 or len(self.animals) >= self.capacity:
            return False

        self.animals.append(Animal(self.db_conn, species, age, name, gender,
            weight))
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

    def simulate(self, interval, period):
        pass
