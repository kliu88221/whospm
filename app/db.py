#Kyle Liu, Yu Lu, Emily Mai, Jun Jie Li
#whospm
#Inspr: snorelacks

import sqlite3
import os
from datetime import datetime
import json

# Database will be stored in Data/database.db >>
DB_NAME = "Data/database.db"
try:
    os.mkdir("Data/")
except:
    pass
DB = sqlite3.connect(DB_NAME)
DB_CURSOR = DB.cursor()

# Create tables >>
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS USER(user_id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS POSTS(post_id INTEGER PRIMARY KEY, pizza_id INTEGER FOREIGN KEY, user_id INTEGER FOREIGN KEY, title TEXT, description TEXT, likes_count INTEGER);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS SAVED_PIZZAS(pizza_id INTEGER PRIMARY KEY, user_id INTEGER FOREIGN KEY, username TEXT, flavor_text TEXT, sauce_name TEXT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS PIZZA_TOPPINGS(entry_id INTEGER PRIMARY KEY, pizza_id INTEGER FOREIGN KEY, topping_id FOREIGN KEY, locationX TEXT, locationY TEXT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS TOPPINGS_MENU(topping_id INTEGER PRIMARY KEY, name INTEGER FOREIGN KEY, topping_id FOREIGN KEY, locationX TEXT, locationY TEXT);")


# Database functions >>
'''
#user stuff
def add_user(username, password):
def get_user(username):

#posts stuff
def add_post(post_id, pizza_id, )

def update_post():

def get_post(username):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT * FROM POSTS WHERE user_id = ?", (user_id,))
#keep user_id or no??\

#pizza stuff
def add_pizza(username, ):
def get_pizza()

#pizza toppings stuff
def add_toppings():

def get_toppings():

#pizza toppings menu stuff
def add_toppingsmenu():

def get_toppingsmenu():


'''



def check_password(username, password):
    return password == get_user(username)[1]
