#!/usr/bin/python3
import sqlite3
import os
import sys
from collections import Counter
import pprint
import juster

def sql_help():
    print("<db> import it rather than use...")
    print("<db> put some useful things here")
    
    
def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path
    
    
'''
def clear_db(dbName="zperson_stuff.db"):
    #it will remove all data and create new db
    try:
        if os.path.exists(dbName):
            os.remove(dbName)       #physically remove db file
        db = sqlite3.connect(dbName)
        c = db.cursor()
        #for table in tables:
        #    print(table[0])
        #    c.execute("DROP TABLE {}".format(table[0]))
        c.execute('CREATE TABLE IF NOT EXISTS {}(data TEXT, national TEXT, sex TEXT)'.format("names"))
        c.execute('CREATE TABLE IF NOT EXISTS {}(data TEXT, national TEXT)'.format("surnames"))
        tables = get_tables(dbName)
        print("<db> database tables: {}".format(tables))
        db.commit()
        c.close()
        db.close()
        print("<db> database file remove and created at new: {}".format(dbName))
        return True
    except:
        print("failed to remove db file: {}".format(dbName))
        return False
'''


def clear_db():
    conn = sqlite3.connect("zperson_stuff.db")
    c = conn.cursor()
    tables = ['names', 'surnames']
    for table in tables:
        c.execute("DROP TABLE {}".format(table))
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
    
    
def remove_national(database):
    ''' remove single national if added in wrong way or something '''
    return True
    
    
def national_db(national):
    ''' get all info about specified national from db '''
    national = national.lower().replace(' ', '_')
    maleNames = data_from_db(TABLE_NAME="names", toGet="data", getBy=[national, "male"])
    maleNames = sorted([item.capitalize() for item in maleNames])
    femaleNames = data_from_db(TABLE_NAME="names", toGet="data", getBy=[national, "female"])
    femaleNames = sorted([item.capitalize() for item in femaleNames])
    surnames = data_from_db(TABLE_NAME="surnames", toGet="data", getBy=[national])
    surnames = sorted([item.capitalize() for item in surnames])
    data = [maleNames, femaleNames, surnames]
    if not any(data):
        # no record for this nationality
        return False
    maxLen = len(max(data, key=len))
    dataExtended = [item + (maxLen-len(item))*[""] for item in data]
    data = list(zip(*dataExtended))
    data.insert(0, ["MALE NAMES", "FEMALE NAMES", "SURNAMES"])
    strData = juster.justify(data, frame=True, enumerator=True, header=True, topbar=national.upper(), justsize=8)
    
    # use juster with no-grid, and with frame; update juster with "list-of-lists" and with enumerator as parameter; ad also header option
    return strData
    
    
def merge_nationals(main, other):
    ''' merge two rows, to one --> "other" will be replaced with "main"'''
    db = sqlite3.connect("zperson_stuff.db")
    c = db.cursor()
    
    
    # ************** get tables **************
    try:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    except sqlite3.DatabaseError as err:
        print("file is not a database...")
        return False
        
    tables = c.fetchall()
    tables = [table for tup in tables for table in tup]
    print(tables)
    
    # ************** do the stuff, iter through tables **************
    for table in tables:
        # replace elements in column nationals --> other, to main, for each table
        sql = 'UPDATE {} SET national = "{}" WHERE national = "{}"'.format(table, main, other)
        print(sql)
        c.execute(sql)
        
    db.commit()
    c.close()
    db.close()
    return True
    
    
def data_from_db(TABLE_NAME, toGet, getBy=False):
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
    
    
def remove_dubles():
    ''' get all data from both tables; remove duplicates; clear db, update db '''
    db = sqlite3.connect("zperson_stuff.db")
    c = db.cursor()
    
    allNames = c.execute('SELECT LOWER({0}), LOWER({1}), LOWER({2}) FROM {3}'.format('data', 'national', 'sex' , 'names'))
    allNames = [item for item in allNames]
    allSurnames = c.execute('SELECT LOWER({0}), LOWER({1}) FROM {2}'.format('data', 'national', 'surnames'))
    allSurnames = [item for item in allSurnames]
    print("before: len(allNames): {}, len(allSurnames): {}".format(len(allNames), len(allSurnames)))
    
    allNamesNoDupli = list(set(allNames))
    allSurnamesNoDupli = list(set(allSurnames))
    print("after: len(allNamesNoDupli): {}, len(allSurnamesNoDupli): {}".format(len(allNamesNoDupli), len(allSurnamesNoDupli)))
    
    
    # clear whole db, table after table
    tables = ['names', 'surnames']
    for table in tables:
        c.execute("DELETE FROM {}".format(table))
    print("clear db made with status: {}".format(True))    
    
    
    # update db with no duplicates data
    c.executemany('INSERT INTO %s VALUES (?,?,?)' % 'names', allNamesNoDupli)
    c.executemany('INSERT INTO %s VALUES (?,?)' % 'surnames', allSurnamesNoDupli)
    print("update db done with status: {}".format(True))
    
    
    db.commit()
    c.close()
    db.close()
    return True
    
    
    
def get_number_of_data():
    ''' return str table which shows the number of items in whole db '''
    db = sqlite3.connect("zperson_stuff.db")
    c = db.cursor()
    namesList = c.execute('SELECT LOWER({0}), {1} FROM {2}'.format('national', 'sex' , 'names'))
    namesList = [x for x in namesList]
    surnamesList = c.execute('SELECT {0} FROM {1}'.format('national', 'surnames'))
    surnamesList = [x[0] for x in surnamesList]
    
    # make str content using juster
    
    # surnamesList
    one = [(*item[0], item[1]) for item in sorted(list(Counter(namesList).items()))]
    two = sorted(list(Counter(surnamesList).items()))
    
    # need to be done
    countries = list(set([item[0] for item in one] + [item[0] for item in two]))
    dataDict = {key: {'male names': '0', 'female names': '0', 'surnames': '0'} for key in countries}
    
    for national, sex, value in one: 
        dataDict[national][sex + ' names'] = str(value)
        
    for national, value in two:
        dataDict[national]['surnames'] = str(value)
    
    data = [(key, *item.values()) for key, item in dataDict.items()]
    
    # need to sort for now
    data = sorted(data)
    data.insert(0, ['NATIONAL', 'MALE NAMES', 'FEMALE NAMES', 'SURNAMES'])
    
    dataStr = '\n'.join([';'.join(item) for item in data])
    justified = juster.justify(dataStr, frame=True)             # here we need to use juster
    
    db.commit()
    c.close()
    db.close()
    # return namesList, surnamesList
    return justified
    
    
def read_file(file_name, rmnl=False):
    '''read specified file and remove newlines depend on "rmnl" parameter'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    path = os.path.join(path, file_name)
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
    '''parse config file, to get table name, and additional data'''
    config = [item.lower() for item in config]      #get it to the floor
    if config:
        table_name = config[0]
        if table_name == "names":
            if len(config) > 2:
                national = config[1]
                sex = config[2]
                if not sex in ("male", "female", "both"):
                    print("<db> wrong sex: {} should be 'male' or 'female'".format(table_name))
                    return "", []
                additional = [national, sex]
            else:
                print("<db> no enough config args: {}".format(config))
                return "", []
        elif table_name == "surnames":
            if len(config) > 1:
                national = config[1]
                additional = [national]
            else:
                print("<db> no enough config args: {}".format(config))
                return "", []                
        else:
            print("<db> wrong table_name: {} should be 'names' or 'surnames'".format(table_name))
            return "", []
        
        return table_name, additional
    else:
        print("<db> no config to parse: {}".format(config))
        return "", []
        
        
def update_db(file, interactive=False):
    '''update database with specified file. Interactive mode is optional'''
    if not os.path.isfile(file):
        print("<db> you specified wrong file: {}".format(file))
        return False
    content = read_file(file, True)
    content = [item.lower() for item in content]        #every line as lowercase
    if not content:
        print("<db> wrong file specified, or empty one")
        return False
    else:
        config = [item.strip() for item in content[0].split(",")]
        data = content[1:]
    table_name, additional = parse_config(config)
    if not table_name or not additional:
        print("<db> wrong config file")
        print("<db> write 1st line, and other data like in example below")
        print("\tnames,poland,male")
        print("\tZenon")
        print("\tLudwik")
        return False
    #replace rubbish:
    toReplace = [",", ".", "/", "\t"]
    for sign in toReplace:
        data = [item.replace(sign, " ") for item in data] 
    
    if interactive:
        #data = [item.replace("/", " ") for item in data]
        print("<db> data format in file:")
        if len(data) > 2:
            for x in range(3):
                print(data[x])
        for item in data:
            #to catch first non-blanc line
            columns = len(item.split())
            if columns:
                break                
        print("<db> columns number:", columns)
        columnNo = input("<db> choose column to update with: 0-{}\n".format(columns))
        appendLast = False
        if additional[-1] == "both":
            appendLast = True
        if not str(columnNo) in [str(x) for x in range(columns)]:
            print("<db> wrong column specified")
            return False
        else:
            columnNo = int(columnNo)
        if appendLast:
            data = [" ".join([item.split()[columnNo], item.split()[-1]]) for item in data if item.strip()]
        else:
            data = [item.split()[columnNo] for item in data if item.strip()]    #'if item' helps with empty lines
            
    db = sqlite3.connect("zperson_stuff.db") #if 1st time it creates new db
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS {}(data TEXT, national TEXT, sex TEXT)'.format("names"))
    c.execute('CREATE TABLE IF NOT EXISTS {}(data TEXT, national TEXT)'.format("surnames"))
    
    #print("--< table_name: {}\n--< additional: {}".format(table_name, additional))

    #remove whitespaces and join additional
    if additional[-1] == "both":
        data = [tuple([item.strip().split()[0], additional[0], item.strip().split()[-1]]) for item in data if item]
        #replaced synonims
        new_data = []
        for item in data:
            #print(item, item[-1].lower(),end="")
            #input()
            if item[-1].lower() in ("boy", "male"):
                new_data.append(tuple(list(item[:-1]) + ["male"]))
                #print("male appended:", tuple(list(item[:-1]) + ["male"]))
            elif item[-1].lower() in ("girl", "female"):
                new_data.append(tuple(list(item[:-1]) + ["female"]))
                #print("female appended:", tuple(list(item[:-1]) + ["female"]))
            else:
                pass
            #print()
            #print()
        data = new_data
        #data = [tuple(item[:2] + "male") if item[2].lower() in ("boy", "male") elif item[2].lower() in ("girl", "female") tuple(item[:2] + "female") else (,) for item in data]
        #print(data)
        #return False
    else:
        data = [tuple([item.strip()] + additional) for item in data if item]        
    data = [tuple([item.capitalize() for item in line[:-1]] + [line[-1]]) for line in data]     #capitalize data except the last one
    print("<db> data to update:\n{}".format(data))
    if input("<db> do you want to update with? (y/n)\n").lower() in "y":
        pass
    else:
        return False

    #return False    #just for debug
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
    # tables = get_tables("zperson_stuff.db")
    
   
'''names & surnames:
https://en.wikipedia.org/wiki/Lists_of_most_common_surnames

https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_Asia
https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_Europe
https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_North_America
https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_Oceania
https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_South_America

https://en.wikipedia.org/wiki/List_of_most_popular_given_names#Americas


tips:
    -sqlite got LOWER function, to convert all selected items to lowercase characters

todo:
    -make tool for merging similar countries like "bosnia-herzegovina" and "bosnia_and_herzegovina", which are the same
    
    
'''


