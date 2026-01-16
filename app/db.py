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
#DB_CURSOR.execute("DROP TABLE IF EXISTS PIZZA_TOPPINGS;")

# Create tables >>
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS USER(user_id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT);")
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS POSTS(post_id INTEGER PRIMARY KEY, pizza_id INTEGER, user_id INTEGER, title TEXT, description TEXT, likes_count INTEGER, FOREIGN KEY(pizza_id) REFERENCES SAVED_PIZZAS(pizza_id), FOREIGN KEY(user_id) REFERENCES USER(user_id));")
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS SAVED_PIZZAS(pizza_id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, flavor_text TEXT, sauce_name TEXT, FOREIGN KEY(user_id) REFERENCES USER(user_id));")
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS PIZZA_TOPPINGS(entry_id INTEGER PRIMARY KEY, pizza_id INTEGER, topping_id INTEGER, locationX TEXT, locationY TEXT, FOREIGN KEY(pizza_id) REFERENCES SAVED_PIZZAS(pizza_id), FOREIGN KEY(topping_id) REFERENCES TOPPINGS_MENU(topping_id));")
#DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS TOPPINGS_MENU(topping_id INTEGER PRIMARY KEY, name TEXT, description TEXT, image_path TEXT);")



# maybe have just username and password, and no user_id ??!
DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS USER(
                    username TEXT PRIMARY KEY,
                    password TEXT);""")

DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS TOPPINGS_MENU(
                    topping_id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    image_url TEXT);""")

DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS SAVED_PIZZAS(
                    pizza_id INTEGER PRIMARY KEY,
                    username TEXT,
                    flavor_text TEXT,
                    sauce_name TEXT,
                    sauce_color TEXT,
                    FOREIGN KEY(username) REFERENCES USER(username));""")


DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS POSTS(
                    post_id INTEGER PRIMARY KEY,
                    pizza_id INTEGER,
                    username TEXT,
                    title TEXT,
                    description TEXT,
                    likes_count INTEGER,
                    FOREIGN KEY(pizza_id) REFERENCES SAVED_PIZZAS(pizza_id),
                    FOREIGN KEY(username) REFERENCES USER(username));""")


DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS PIZZA_TOPPINGS(
                    entry_id INTEGER PRIMARY KEY,
                    pizza_id INTEGER,
                    topping_id INTEGER,
                    locationX TEXT,
                    locationY TEXT,
                    FOREIGN KEY(pizza_id) REFERENCES SAVED_PIZZAS(pizza_id),
                    FOREIGN KEY(topping_id) REFERENCES TOPPINGS_MENU(topping_id));""")


# wtf lol
DB_CURSOR.execute("""INSERT OR IGNORE INTO TOPPINGS_MENU VALUES(
                  1,
                  'Pepperoni',
                  'salty too oily yum yum red circles',
                  '/static/img/pepperoni.png');""")
DB_CURSOR.execute("""INSERT OR IGNORE INTO TOPPINGS_MENU VALUES(
                  2,
                  'Pineapple',
                  'sweet yellow chunks. do they belong here?',
                  '/static/img/pineapple.png');""")
DB_CURSOR.execute("""INSERT OR IGNORE INTO TOPPINGS_MENU VALUES(
                  3,
                  'Ham',
                  'non circle salty yum yums',
                  '/static/img/ham.png');""")

DB_CURSOR.execute("""INSERT OR IGNORE INTO TOPPINGS_MENU VALUES(4, 'Mushroom', 'ts so bad', '/static/img/mushroom.png');""")

DB_CURSOR.execute("""INSERT OR IGNORE INTO TOPPINGS_MENU VALUES(5, 'Demon', '.̸͍͕̍̾̅̃.̵͕̼̇̿̈̀͆̄̾͊͝.̸̨̛̞́̑͗͑̄̒́̒̔̃̀̂ͅ.̶̨̛̛̘͙͍͚̥͉̝͔̥̀͛̾̌̐̊̍̉̎̕͠.̶̢̦̝͍͎̳̹̤̝͔̌͜͝.̷̢̛̮͈͉͓̘̖̥̟́͑͛̓̾̊̾͝.̷̨̻͍̥͆̒̇.̸̛̯͇̬̮̻͉̹̊͒̑̔́̎͌̀̊̑̂̂͊.̵̡̢̯̼͓̦̝̯̱̹̯̻̣́̾̓͌͒͗̊̌͋̓̌̂͛͝.̵̧͓̥̹̪̯̅̑̒͒̚̚.̷̡͔̣̤̞̙̬̺̩̦̾̈́͆̔̏̎̋͛̊͝...?', '/static/img/demon.png');""")

DB_CURSOR.execute("""INSERT OR IGNORE INTO TOPPINGS_MENU VALUES(6, 'Cheese', 'Get that 2nd cup o-cheese yeaa', '/static/img/cheese.png');""")
                  
DB.commit()
DB.close()
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
    DB_CURSOR.execute("SELECT * FROM USER WHERE username = ?", (username,))
    cursorfetch = DB_CURSOR.fetchone()
    DB.close()
    return cursorfetch

def check_password(username, password):
    return password == get_user(username)[1]


#posts stuff
def create_post(username, pizza_id, title, description):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    #check to see if pizza belongs to the user
    DB_CURSOR.execute("SELECT 1 FROM SAVED_PIZZAS WHERE pizza_id = ? AND username = ?", (pizza_id, username))
    row = DB_CURSOR.fetchone()
    if row is None:
        DB.close()
        return False
    #add post
    DB_CURSOR.execute("INSERT INTO POSTS (pizza_id, username, title, description, likes_count) VALUES (?, ?, ?, ?, ?)", (pizza_id, username, title, description, 0))
    DB.commit()
    DB.close()
    return True

#return dictionary of post information
def get_post(post_id):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()

    post = DB_CURSOR.execute("SELECT post_id, pizza_id, username, title, description, likes_count FROM POSTS WHERE post_id = ?", (post_id,)).fetchone()
    if post is None:
        return None

    pizza = get_pizza(post[1])
    return {
        "post_id": post[0],
        "username": post[2],
        "title": post[3],
        "description": post[4],
        "likes_count": post[5],
        "pizza": pizza
    }

#pizza stuff
def save_pizza(username, sauce_name, sauce_color, toppings_list):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    flavor_text = "Is this what makes the best pizza maker?" #we can add a user input for this later and make this the base msg
    DB_CURSOR.execute("INSERT INTO SAVED_PIZZAS (username, flavor_text, sauce_name, sauce_color) VALUES (?, ?, ?, ?)", (username, flavor_text, sauce_name, sauce_color))
    pizza_id = DB_CURSOR.lastrowid
    for topping in toppings_list:
        DB_CURSOR.execute("INSERT INTO PIZZA_TOPPINGS (pizza_id, topping_id, locationX, locationY) VALUES (?, ?, ?, ?)", (pizza_id, topping['id'], str(topping['x']), str(topping['y'])))
    DB.commit()
    DB.close()
    return pizza_id

#return dictionary of pizza info with toppings
def get_pizza(pizza_id):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()

    #check if pizza_id is valid
    pizza = DB_CURSOR.execute("SELECT pizza_id, username, flavor_text, sauce_name, sauce_color FROM SAVED_PIZZAS WHERE pizza_id = ?", (pizza_id,)).fetchone()
    if pizza is None:
        DB.close()
        return False

    toppings = DB_CURSOR.execute(
    """ SELECT
        pt.entry_id,
        pt.topping_id,
        tm.name,
        tm.image_url,
        pt.locationX,
        pt.locationY
        FROM PIZZA_TOPPINGS pt
        JOIN TOPPINGS_MENU tm
        ON pt.topping_id = tm.topping_id
        WHERE pt.pizza_id = ?
        """,
        (pizza_id,)
    ).fetchall()
    DB.close()

    return {
        "pizza_id": pizza[0],
        "username": pizza[1],
        "flavor_text": pizza[2],
        "sauce_name": pizza[3],
        "sauce_color": pizza[4],
        "toppings": [
            {
                "entry_id": t[0],
                "topping_id": t[1],
                "name": t[2],
                "image_url": t[3],
                "x": t[4],
                "y": t[5]
            }
            for t in toppings
        ]
    }

def get_pizza_all():
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    
    DB_CURSOR.execute("SELECT pizza_id FROM SAVED_PIZZAS ORDER BY pizza_id DESC")
    rows = DB_CURSOR.fetchall()
    DB.close()
    
    results = []
    if rows:
        for p in rows:
            pizza = get_pizza(p[0])
            if pizza:
                if len(pizza['toppings']) > 0:
                    first = pizza['toppings'][0]['topping_id']
                    pizza['flavor_highlight'] = get_topping_description(first)
                else:
                    pizza['flavor_highlight'] = "Yeah, looks like a delious piza to me :)"
                
                results.append(pizza)
    return results

def get_topping_description(topping_id):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    
    DB_CURSOR.execute("SELECT description FROM TOPPINGS_MENU WHERE topping_id = ?", (topping_id,))
    row = DB_CURSOR.fetchone()
    
    DB.close()
    if row:
        return row[0]
    return "Yeah, looks like a delious piza to me :)"

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
