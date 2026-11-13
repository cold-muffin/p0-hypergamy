#Wenjie Ma
#Software Development
#skeleton/stub :: SQLITE3 BASICS
#Oct 2026

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#==========================================================
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
< < < INSERT YOUR TEAM'S DB-POPULATING CODE HERE > > >
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below, you will find a bit more scaffolding.
USAGE:
As you address each piece of functionality,
 "talk shop" as you design it,
 TEST it in sqlite3 shell,
 then...
"""

command = '''CREATE TABLE IF NOT EXISTS
roster(name TEXT, age INTEGER, id INTEGER)
'''          # <-- insert tested stmt in quotes
c.execute(command)    # run SQL statement

with open('students.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c.execute(
    "INSERT INTO roster (name, age, id) VALUES (?, ?, ?)",
    (row['name'], row['age'], row['id'])
)
c.execute("CREATE TABLE IF NOT EXISTS courses(code TEXT, mark INTEGER, id INTEGER)")
with open('courses.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c.execute(
    "INSERT INTO courses (code, mark, id) VALUES (?, ?, ?)",
    (row['code'], row['mark'], row['id'])
    )

#use placeholders to avoid fstrings
#python -m sqlite3 your_database.db
c.execute("SELECT * FROM roster;")
#==========================================================

db.commit() #save changes
db.close()  #close database
