#!/usr/bin/python3
import sqlite3
import os
import sys

def sql_help():
    print("import it rather than use...")
    print("put some useful things here")
'''
def create_table(c, TABLE_NAME = "name"):
    c.execute('CREATE TABLE IF NOT EXISTS %s(name TEXT, nationality TEXT, sex TEXT)' % TABLE_NAME)

def data_entry(c, DATA, TABLE_NAME):
    c.executemany('INSERT INTO %s VALUES (?,?,?)' % TABLE_NAME, DATA)

def get_data(db, c, TABLE_NAME, COLUMN_IN, COLUMN_OUT):
    #put some case statement to choose only what we need rather than thousands of arguments
    data = c.execute('SELECT %s FROM %s WHERE sex="%s"' % (COLUMN_IN, TABLE_NAME, COLUMN_OUT))
    data = list(data)
    #dataOut = [x for x in data]
    return data
'''

def script_path(fileName=''):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    if fileName:
        fullPath = os.path.join(path, fileName)
        return fullPath
    return path

def clear_db(dbName="zperson_stuff.db"):
    #it will remove all data and create new db
    db = sqlite3.connect(dbName)
    c = db.cursor()
    tables = get_tables(dbName)
    print(tables)
    for table in tables:
        print(table[0])
        c.execute('''DROP TABLE {}'''.format(table[0]))
    c.execute('CREATE TABLE IF NOT EXISTS {}(data TEXT, national TEXT, sex TEXT)'.format("names"))
    c.execute('CREATE TABLE IF NOT EXISTS {}(data TEXT, national TEXT)'.format("surnames"))
    db.commit()
    c.close()
    db.close()        
    return True
    
def get_tables(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    except sqlite3.DatabaseError as err:
        print("file is not a database...")
        return False
    tables = c.fetchall()
    return tables
    
#def get_data(TABLE_NAME, toGet="", getBy=""
def data_from_db(TABLE_NAME, toGet, getBy=[]):
    db = sqlite3.connect("zperson_stuff.db")
    c = db.cursor()
    if not getBy:
        data = c.execute('SELECT {0} FROM {1}'.format(toGet, TABLE_NAME))
    else:
        if TABLE_NAME == "names":
            #data = c.execute('SELECT {0} FROM {1} WHERE national={2} AND sex={3}'.format(toGet, TABLE_NAME, getBy[0], getBy[1]))
            data = c.execute('SELECT {0} FROM {1} WHERE national="{2}" AND sex="{3}"'.format(toGet, TABLE_NAME, getBy[0], getBy[1]))
        elif TABLE_NAME == "surnames":
            data = c.execute('SELECT {0} FROM {1} WHERE national="{2}"'.format(toGet, TABLE_NAME, getBy[0]))
    dataOut = [x[0] for x in data]
    db.commit()
    c.close()
    db.close()  
    return dataOut

'''    
def get_all(db, c, TABLE_NAME):
    data = c.execute('SELECT * FROM %s' % (TABLE_NAME))
    for item in data:
        print(item)
    return data
'''

def read_file(fileName, rmnl=False):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    path = os.path.join(path, fileName)
    try:
        with open(path, "r") as file:
            if rmnl:
                fileContent = file.read().splitlines()
            else:
                fileContent = file.readlines()
    except:
        fileContent = []
    return fileContent    

def parse_config(config):
    config = [item.lower() for item in config]      #get it to the floor
    if config:
        table_name = config[0]
        if table_name == "names":
            if len(config) > 2:
                national = config[1]
                sex = config[2]
                if not sex in ("male", "female"):
                    print("wrong sex: {} should be 'male' or 'female'".format(table_name))
                    return "", []
                additional = [national, sex]
            else:
                print("no enough config args: {}".format(config))
                return "", []
        elif table_name == "surnames":
            if len(config) > 1:
                national = config[1]
                additional = [national]
            else:
                print("no enough config args: {}".format(config))
                return "", []                
        else:
            print("wrong table_name: {} should be 'names' or 'surnames'".format(table_name))
            return "", []
        
        return table_name, additional
    else:
        print("no config to parse: {}".format(config))
        return "", []
        
def update_db(file):
    if not os.path.isfile(file):
        print("you specified wrong file: {}".format(file))
        return False
    content = read_file(file, True)
    if not content:
        print("wrong file specified, or empty one")
        return False
    else:
        config = content[0].split(",")
        data = content[1:]

    db = sqlite3.connect("zperson_stuff.db") #if 1st time it creates new db
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS {}(data TEXT, national TEXT, sex TEXT)'.format("names"))
    c.execute('CREATE TABLE IF NOT EXISTS {}(data TEXT, national TEXT)'.format("surnames"))
    
  
    table_name, additional = parse_config(config)
    #print("--< table_name: {}\n--< additional: {}".format(table_name, additional))
    if not table_name or not additional:
        print("--< wrong config file")
        print("--< write 1st line, and other data like in example below")
        print("\tnames,polish,male")
        print("\tZenon")
        print("\tLudwik")
        return False
    else:
        #remove whitespaces and join additional
        data = [tuple([item.strip()] + additional) for item in data if item]        
        print("--< data to update:\n{}".format(data))       
    
    if table_name == "names":
        c.executemany('INSERT INTO %s VALUES (?,?,?)' % table_name, data)
    elif table_name == "surnames":
        c.executemany('INSERT INTO %s VALUES (?,?)' % table_name, data)
    else:
        return False
    
    db.commit()
    c.close()
    db.close()        
    return True
    
    
if __name__ == "__main__":
    #path = script_path()
    #clear_db()
    sql_help()
    
    
    
    