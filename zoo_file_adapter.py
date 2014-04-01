from zoo import Zoo
from animals import Animal


class ZooFileAdapter():
    def __init__(self, db_conn, zoo):
        self.db_conn = db_conn
        self.zoo = zoo

        self._ensure_table_exists()

    def _ensure_table_exists(self):
        create_table = '''create table if not exists
                          zoos(id integer primry key,
                                capacity int,
                                budget int)'''
        cursor = self.db_conn.cursor()
        cursor.execute(create_table)

    def save(self):
        if self.zoo.get_id() == -1:
            add_zoo = 'insert into zoos(capacity, budget) VALUES(?, ?)'
            cursor = self.db_conn.execute(add_zoo,
                    (self.zoo.capacity, self.zoo.budget))
            self.zoo.set_id(cursor.lastrowid)

            for animal in self.zoo.animals:
                pass
        else:
            pass

    def load(self, load_id=-1):
        pass
