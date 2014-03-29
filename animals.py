import sqlite3
from random import randint


class Animal():
	"""docstring for Animal"""
	def __init__(self, db_conn, species, age, name, gender, weight):
		self.species = species
		self.age = age
		self.name = name
		self.gender = gender
		self.weight = weight
		self.db_conn = db_conn
		
	def grow(self):
		self.age += 1
		sql_avarage = "SELECT average_weight, weight_age_ratio FROM animals WHERE species = ?"
		cursor = conn.cursor()
		sql_result = cursor.execute(sql_avarage).fetchone()
		if sql_avarage[0] > self.weight:
			self.weight += weight_age_ratio[1]
	
	def eat(self):
		sql_avarage = "SELECT average_weight, food_weight_ratio FROM animals WHERE species = ?"
		cursor = conn.cursor()
		sql_result = cursor.exeute(sql_avarage).fetchone()
		if self.weight < sql_avarage[0]:
			self.weight += sql_avarage[1]

	def die(self):
		sql_avarage = "SELECT life_expectanct FROM animals WHERE species = ?"
		rand_koef = randint(1,3)
		chance = 100//(life_expectanct[0] - self.age/12 + rand_koef)
		rand_die = randint(1,100)
		if rand_die <= chance:
			return True
		else:
			return False