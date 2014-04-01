from animals import Animal
import sqlite3


class AnimalFileAdapter():
    """docstring for AnimalFileAdapter"""
    def __init__(self, db_conn, animal):
        self.db_conn = db_conn
        self.animal = animal
        self._ensure_table_exists()

    def prepare_to_save(self):
        return (self.animal.name, self.animal.species, self.animal.age,
                self.animal.gender, self.animal.weight)

    def _ensure_table_exists(self):
        create_table = '''CREATE TABLE IF NOT EXISTS
            animals(id INTEGER PRIMARY KEY,
                    name text,
                    species text,
                    age int,
                    gender text,
                    weight float)'''
        cursor = self.db_conn.cursor()
        cursor.execute(create_table)

    def save(self):
        cursor = self.db_conn.cursor()

        if self.animal.get_id() == -1:
            add_animal = '''INSERT INTO animals(name,species,age,gender,weight)
                VALUES(?, ?, ?, ?, ?)'''
            cursor.execute(add_animal, self.prepare_to_save())
            self.animal.set_id(cursor.lastrowid)
        else:
            update_animal = '''update animals set name=?, species=?, age=?,
                gender=?, weight=? where id=?'''
            cursor.execute(update_animal, self.prepare_to_save() +
                    (self.animal.get_id(), ))

    def load(self, load_id=-1):
        request_id = -1
        if self.animal.get_id() > 0:
            request_id = self.animal.get_id()
        elif load_id > 0:
            request_id = load_id
        else:
            return False

        get_animal = 'select * from animals where id=?'
        cursor = self.db_conn.cursor()
        result = cursor.execute(get_animal, (request_id, )).fetchone()

        self.animal.name = result[1]
        self.animal.species = result[2]
        self.animal.age = result[3]
        self.animal.gender = result[4]
        self.animal.weight = result[5]
        return True

