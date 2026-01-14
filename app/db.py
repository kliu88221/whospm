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

# Delete tables
DB_CURSOR.execute("DROP TABLE IF EXISTS USER;")
DB_CURSOR.execute("DROP TABLE IF EXISTS POSTS;")
DB_CURSOR.execute("DROP TABLE IF EXISTS SAVED_PIZZAS;")
DB_CURSOR.execute("DROP TABLE IF EXISTS TOPPINGS_MENU;")

# Create tables >>
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS USER(user_id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT);")
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS POSTS(post_id INTEGER PRIMARY KEY, pizza_id INTEGER, user_id INTEGER, title TEXT, description TEXT, likes_count INTEGER, FOREIGN KEY(pizza_id) REFERENCES SAVED_PIZZAS(pizza_id), FOREIGN KEY(user_id) REFERENCES USER(user_id));")
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS SAVED_PIZZAS(pizza_id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, flavor_text TEXT, sauce_name TEXT, FOREIGN KEY(user_id) REFERENCES USER(user_id));")
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS PIZZA_TOPPINGS(entry_id INTEGER PRIMARY KEY, pizza_id INTEGER, topping_id INTEGER, locationX TEXT, locationY TEXT, FOREIGN KEY(pizza_id) REFERENCES SAVED_PIZZAS(pizza_id), FOREIGN KEY(topping_id) REFERENCES TOPPINGS_MENU(topping_id));")
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS TOPPINGS_MENU(topping_id INTEGER PRIMARY KEY, name TEXT, description TEXT, image_url TEXT);")



# maybe have just username and password, and no user_id ??!
DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS USER(
                    username TEXT PRIMARY KEY,
                    password TEXT);""")

DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS POSTS(
                    post_id INTEGER PRIMARY KEY,
                    pizza_id INTEGER,
                    username TEXT,
                    title TEXT,
                    description TEXT,
                    likes_count INTEGER,
                    FOREIGN KEY(pizza_id) REFERENCES SAVED_PIZZAS(pizza_id),
                    FOREIGN KEY(username) REFERENCES USER(username));""")

DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS SAVED_PIZZAS(
                    pizza_id INTEGER PRIMARY KEY,
                    username TEXT,
                    flavor_text TEXT,
                    sauce_name TEXT,
                    FOREIGN KEY(username) REFERENCES USER(username));""")

DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS PIZZA_TOPPINGS(
                    entry_id INTEGER PRIMARY KEY,
                    pizza_id INTEGER,
                    topping_id INTEGER,
                    locationX TEXT,
                    locationY TEXT,
                    FOREIGN KEY(pizza_id) REFERENCES SAVED_PIZZAS(pizza_id),
                    FOREIGN KEY(topping_id) REFERENCES TOPPINGS_MENU(topping_id));""")

DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS TOPPINGS_MENU(
                    topping_id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    image_url TEXT);""")


# Database functions >>
#user stuff
def add_user(username, password):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT COUNT(*) FROM USER WHERE username = (?)", (username,))
    cursorfetch = DB_CURSOR.fetchone()[0]
    if cursorfetch == 1:
        DB.commit()
        DB.close()
        return False
    DB_CURSOR.execute("INSERT INTO USER VALUES(?, ?)", (username, password))
    DB.commit()
    DB.close()
    return True

def get_user(username):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT * FROM Users WHERE username = ?", (username,))
    cursorfetch = DB_CURSOR.fetchone()
    return cursorfetch

def check_password(username, password):
    return password == get_user(username)[1]


#posts stuff
def add_post(post_id, pizza_id, username, title, description, likes_count):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("INSERT INTO POSTS(?, ?, ?, ?, ?, ?)", (post_id, pizza_id, username, title, description, likes_count))
    DB.commit()
    DB.close()
    return True
'''
def edit_post(post_id, ):

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
