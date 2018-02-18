#!/usr/bin/python3
import sqlite3
import os

def create_table(c, TABLE_NAME = "name"):
    c.execute('CREATE TABLE IF NOT EXISTS %s(name TEXT, nationality TEXT, sex TEXT)' % TABLE_NAME)

def data_entry(c, DATA, TABLE_NAME):
    #c.execute('INSERT INTO names VALUES (?,?,?)', ("Xavier", "Spain", "male"))
    c.executemany('INSERT INTO %s VALUES (?,?,?)' % TABLE_NAME, DATA)
    #db.commit() #save changes
    #db.close()

def get_data(db, c):
    data = c.execute('SELECT nationality FROM name WHERE sex="%s"' % "female")
    #data = c.execute('SELECT * FROM name')
    for item in data:
        print(item)
    db.commit()
    db.close()

def read_file(fileName, rmnl=False):
    try:
        os.chdir(os.path.dirname(__file__))
    except:
        os.path.dirname(os.path.abspath(__file__))
    pathAbs = os.getcwd()
    path = os.path.join(pathAbs, fileName)
    fileContent = []
    try:
        with open(path, "r", encoding='utf-8') as file:
            if rmnl:
                fileContent = file.read().splitlines()
            else:
                fileContent = file.readlines()
    except UnicodeDecodeError as err:
        print("Exception:\n\t", err)
    return fileContent

def sort_data(content):
    info = content[0].split(',')
    if len(info)!=3:
        return [], []
    data = [(x.strip(),info[1],info[2]) for x in content[1:] if x]  #if x removes empty strings; x.strip() remove whitespace
    #read data from file
    #file structure:
    #   table_name,nationality,sex
    #   value1
    #   value2
    #-----------------------------
    #return info(1st-line-from-file), data(other-lines)
    return info[0], data

def update_db(filename):
    DATA = []
    db = sqlite3.connect("ALL_DATA.db") #if 1st time it creates new db
    c = db.cursor()
    file_content = read_file(filename, rmnl=True)
    if not file_content:
        print("empty file...")
        return False
    TABLE_NAME, DATA = sort_data(file_content)
    if TABLE_NAME and DATA:
        create_table(c, TABLE_NAME)
        data_entry(c, DATA, TABLE_NAME)
        get_data(db, c)
        #db.executemany() #put data into db
    else:
        print("faulty file format. could not update db")
    #in case of not exists file or bad format return False; in other case read file, sort data and update database

if __name__ == "__main__":
    '''
    db = sqlite3.connect("surnames.db")
    c = db.cursor()
    create_table("names")
    data_entry()
    get_data()
    '''

    content = ["nazwa,spanish,female", "xandra", "elize", "honorita", "Anastasia", "Alba", "Agueda"]
    data = sort_data(content)
    print(data)
