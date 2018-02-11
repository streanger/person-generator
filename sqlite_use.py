#!/usr/bin/python3
import sqlite3


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS names(position INT, name TEXT, nationality TEXT, sex TEXT, lenght INT)')

def data_entry():
    c.execute('INSERT INTO names VALUES (?,?,?,?,?)', (1, "Xavier", "Spain", "male", len("Xavier")))
    #db.commit() #save changes
    #db.close()

def get_data():
    #data out
    data = c.execute('SELECT nationality FROM names WHERE sex="%s"' % "female")
    data = c.execute('SELECT * FROM names')
    for item in data:
        print(item)
    #print(data)
    db.commit()
    db.close()


if __name__ == "__main__":
    print(42)
    db = sqlite3.connect("names.db")
    c = db.cursor()
    create_table()
    data_entry()
    get_data()
