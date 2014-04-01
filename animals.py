import sqlite3
from random import randint


class Animal():
    """docstring for Animal"""
    def __init__(self, db_conn, species, age, name, gender):
        self.__id = -1
        self.species = species
        self.age = age
        self.name = name
        self.gender = gender
        self.db_conn = db_conn

        cursor = self.db_conn.cursor()
        sql_a_to_w = '''SELECT weight_age_ratio, average_weight FROM animals
                        WHERE species = ?'''
        sql_result = cursor.execute(sql_a_to_w, (self.species, )).fetchone()
        age_to_weight = sql_result[0]
        self.weight = self.age * age_to_weight
        if self.weight > sql_result[1]:
            self.weight = sql_result[1]
        elif self.weight == 0:
            self.weight = age_to_weight

    def get_id(self):
        return self.__id

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def get_name(self):
        return self.name

    def set_id(self, new_id):
        self.__id = new_id

    def grow(self):
        self.age += 1
        sql_avarage = '''SELECT average_weight, weight_age_ratio FROM animals
                         WHERE species = ?'''
        cursor = self.db_conn.cursor()
        sql_result = cursor.execute(sql_avarage, (self.species,)).fetchone()
        if sql_result[0] > self.weight:
            self.weight += sql_result[1]

    def eat(self):
        sql_avarage = '''SELECT average_weight, food_weight_ratio FROM animals
                         WHERE species = ?'''
        cursor = self.db_conn.cursor()
        sql_result = cursor.exeute(sql_avarage, (self.species,)).fetchone()
        if self.weight < sql_result[0]:
            self.weight += sql_result[1]

    def die(self):
        sql_avarage = 'SELECT life_expectancy FROM animals WHERE species = ?'
        cursor = self.db_conn.cursor()
        sql_result = cursor.execute(sql_avarage, (self.species,)).fetchone()
        chance = self.age / sql_result[0]
        rand_die = randint(1,100)

        if rand_die <= chance*100:
            return True
        else:
            return False

    def get_gestation_period(self):
        sql = 'SELECT gestation FROM animals WHERE species=?'
        cursor = self.db_conn.cursor()
        gestation = cursor.execute(sql, (self.species, )).fetchone()[0]
        return gestation

    def food_for_day(self):
        sql = 'SELECT food_weight_ratio FROM animals WHERE species = ?'
        cursor = self.db_conn.cursor()
        sql_result = cursor.execute(sql, (self.species,)).fetchone()
        return int(self.weight * sql_result[0] * 100) / 100