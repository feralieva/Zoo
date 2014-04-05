from zoo import Zoo
from animals import Animal
from animals_file_adapter import AnimalFileAdapter


class ZooFileAdapter():
    def __init__(self, db_conn, zoo):
        self.db_conn = db_conn
        self.zoo = zoo

        self._ensure_table_exists()

    def _ensure_table_exists(self):
        create_table = '''CREATE TABLE IF NOT EXISTS
                          zoos(id INTEGER PRIMARY KEY,
                                capacity int,
                                budget int)'''
        cursor = self.db_conn.cursor()
        cursor.execute(create_table)

    def save(self):
        if self.zoo.get_id() == -1:
            add_zoo = 'INSERT INTO zoos(capacity, budget) VALUES(?, ?)'
            cursor = self.db_conn.cursor()
            cursor.execute(add_zoo, (self.zoo.capacity, self.zoo.budget))
            self.zoo.set_id(cursor.lastrowid)
        else:
            update_zoo = 'UPDATE zoos SET budget=?, capacity=?'
            cursor = self.db_conn.cursor()
            cursor.execute(update_zoo, (self.zoo.budget, self.zoo.capacity))

        for animal in self.zoo.animals:
            animal_adapter = AnimalFileAdapter(self.db_conn, animal)
            animal_adapter.save()

    def load(self, load_id=-1):
        req_id = -1
        if self.zoo.get_id() > 0:
            req_id = self.zoo.get_id()
        elif load_id > 0:
            req_id = load_id
        else:
            return False

        get_zoo = 'SELECT * FROM zoos WHERE id=?'
        cursor = self.db_conn.cursor()
        result = cursor.execute(get_zoo, (req_id,)).fetchone()

        self.zoo.capacity = result[1]
        self.zoo.budget = result[2]
        
        animal_from_zoo = 'SELECT id FROM zoo_animals WHERE id=?'
        animal_cursor = self.db_conn.cursor()
        anim_result = animal_cursor.execute(animal_from_zoo, (req_id,))
        for row in anim_result:
            animal = Animal(self.db_conn, 'tiger', 0, '', '')
            id_animal = animal.set_id(row[0])
            animal_adapter = AnimalFileAdapter(self.db_conn, animal)
            animal_adapter.load(id_animal)
        return True