#Kyle Liu, Yu Lu, Emily Mai, Jun Jie Li
#whospm

# Imports >>
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import db
import json
from urllib.request import Request, urlopen
import pprint
import os
import re

# Initialize DB >>

# Create instance of Flask app >>
app = Flask(__name__)
app.secret_key = "ABCEDFGHIJKLMNOPQRSTUVWXYZ1234567890987654321"

@app.context_processor
def user_context(): # persistent info made avalible for all html templates
    return {
        "logged_in": ('username' in session), # eventually change requirement to userid after db is done
        "current_user": session.get('username')
    }

#@app.before_request

# ROUTING BEGINS >>

@app.route("/", methods=['GET', 'POST'])
def homepage():
    flash("Welcome to Whospm!")
    x = 1
    results = []
    while(True):
        ret = db.get_pizza(x)
        print(ret)
        if(ret):
            results.append(ret)
            x += 1
        else:
            break
    return render_template("homepage.html", results=results)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username'].strip()
        pswd = request.form['password'].strip()
        nation = None
        money = None

        if(not user or not pswd):
            flash("WARNING: One of the fields cannot be empty!")
            return redirect(url_for('register'))

        # add database registration here
        if db.add_user(user, pswd):
            flash(f"Registration Successful! Welcome, {user}. Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Username already exists. Please choose another.")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username'].strip()
        pswd = request.form['password'].strip()
        if(not user or not pswd):
            flash("WARNING: Username and Password cannot be empty!")
            return redirect(url_for('login'))

        # add database authentication here
        db_user = db.get_user(user)
        if (db_user is None or not db.check_password(user,pswd)):
            flash("Username or password is not correct!")
            return redirect(url_for('login'))
        flash(f"Login Successful! Welcome back, {user}.")

        session['username'] = user
        return redirect(url_for('canvas'))
    return render_template("login.html")

@app.route("/logout") # link jinja template to this route via button
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('homepage'))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    user = session.get('username')
    if (not user):
        flash("You are not logged in!")
        return redirect(url_for('login'))

    db_user = db.get_user(user)

    return render_template("profile.html", db_user = db_user)

@app.route("/canvas", methods=['GET', 'POST'])
def canvas():
    return render_template("canvas.html")


@app.route('/db/save_pizza', methods=['POST'])
def save_pizza_api():
    data = request.get_json()

    print("Received Pizza Data:", data)

    if 'username' not in session:
        return {"status": "error", "message": "Not logged in"}, 401

    username = session.get('username')
    sauce_name = data['sauce']['name']
    sauce_color = data['sauce']['color']
    toppings = data['toppings']

    pizza_id = db.save_pizza(username, sauce_name, sauce_color, toppings)

    return {"status": "success", "message": "Pizza saved!", "pizza_id": pizza_id}, 200


if __name__ == "__main__":
    app.debug = True
    app.run()
