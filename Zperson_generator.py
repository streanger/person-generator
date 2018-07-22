#!/usr/bin/python3
#it would be useful with generate random person data
#11.02.18 -> it still need a lot of work :(
import os
import random
import sys
import shutil   #download_image
import requests #download_image
import getopt
import logging

#own modules
import sqlite_use as sql
from random_data import get_email, random_date, get_age, random_phone


def download_image(url, fileName="image.png"):
    #will download&save image under specified address
    #url = 'http://ontheedge.hol.es/codeEffects/chooseBg.png'
    try:
        response = requests.get(url, stream=True)
        with open(fileName, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            logging.info("--< image written to: %s" % fileName)
    except:
        logging.warning("Wrong url")
    del response
    
def script_path(fileName=''):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    if fileName:
        fullPath = os.path.join(path, fileName)
        return fullPath
    return path

def remove_duplicates(someList, sort=True):
    return list(set(someList))

def read_file(fileName, rmnl=False):
    path = os.path.join(PATH, fileName)
    try:
        with open(path, "r") as file:
            if rmnl:
                fileContent = file.read().splitlines()
            else:
                fileContent = file.readlines()
    except:
        fileContent = []
    return fileContent
    
def write_file(fileName, content, endline="\n", overWrite=False, response=True, rmSign=[]):
    if not content:
        return False
    contentType = type(content)
    if contentType in (list, tuple):
        pass
    elif contentType in (int, str):
        content = [str(content)]
    elif contentType is (dict):
        content = list(content.items())
    else:
        return False
    if overWrite:
        mode="w"
    else:
        mode="a"
    path = os.path.join(PATH, fileName)
    with open(path, mode) as file:
        for item in content:
            if rmSign:
                for sign in rmSign:
                    item = (str(item)).replace(sign, "")
            file.writelines(str(item)+endline)
        file.close()
        if response:
            print("--< written to: {0} | contentType: {1}".format(fileName, contentType))
    return True

def write_names(names):
    for key, item in enumerate(names):
        write_file("name" + str(key) + ".txt", item, addNewline=True, overWrite=True, subPath="")
    return 0

def get_data(key, personDictio):
    #return specified data with using proper functions
    #data = "Random"
    if key == "Nationality":
        nationalList = sql.data_from_db("names", "national") + sql.data_from_db("surnames", "national")
        nationalList = list(set(nationalList))
        if not nationalList:
            nationalList = ["Random"]
        data = random.choice(nationalList)
    elif key == "Name":
        national = personDictio["Nationality"]
        sex = personDictio["Sex"]
        names = sql.data_from_db(TABLE_NAME="names", toGet="data", getBy=[national, sex])
        if not names:
            names = ["Random"]
        #print(names)
        data = random.choice(names)
    elif key == "Surname":
        national = personDictio["Nationality"]
        surnames = sql.data_from_db(TABLE_NAME="surnames", toGet="data", getBy=[national])
        if not surnames:
            surnames = ["Random"]
        #print(surnames)
        data = random.choice(surnames)
    #elif key == "Birthdate":
    #    data = random_date(age=val)
    elif key == "Age":
        data = get_age(personDictio["Birthdate"])
    elif key == "Email":
        data = get_email(personDictio)
    elif key == "Phone":
        data = str(random_phone())
    else:
        data = "Random"
    return data

def capitalize_dictio(dictio):
    for key,val in dictio.items():
        if key == "Email":
            continue
        if type(val) is str:
            dictio[key] = val.capitalize()
    return dictio
    
def usage():
    print("usage:")
    print("-u <fileName> - file with data to update database")
    print("-n <nationality> - nationality of person to generate [default=english]")
    print("-s <sex> - gender of person to generate [default=male]")
    print("-q <quantity> - the number of persons(s) to generate [default=1]")
    print("-a <age> - age of person(s)")
    print("-r - random nationality and sex")
    print("-h - this usage help")
    print("--"*35)
    return True
    
def generate_person(national="Random", sex="Random", age=0, writeFile=True):
    personDataDictio = { "Nationality" : "Random",
                         "Sex" : "Random",
                         "Name" : "Random",
                         "Surname" : "Random",
                         "Birthdate" : "Random",
                         "Age" : "Random",
                         "Email" : "Random",
                         "Phone" : "Random"}
    personData = {}
    if national == "Random":
        personData["Nationality"] = get_data("Nationality", personData)
    else:
        personData["Nationality"] = national
    if sex == "Random":
        personData["Sex"] = random.choice(["male", "female"])
    else:
        personData["Sex"] = sex
    personData["Birthdate"] = random_date(age=age)
    otherData = ["Name", "Surname", "Age", "Email", "Phone"]
    for key in otherData:
        personData[key] = get_data(key, personData)
    personData = capitalize_dictio(personData)
    return personData

def show_data(dictio, dataType=0):
    if dataType == 0:
        return "\n".join(dictio.values())
    elif dataType == 1:
        return "\n".join("{}".format(item) for item in dictio.items())
    elif dataType == 2:
        return "\n".join("{}: {}".format(key, item) for key, item in dictio.items())
    else:
        return "\n".join(dictio.values())
        
def main(argv):
    #check if db exists and
    tables = sql.get_tables("zperson_stuff.db")
    if tables != [("names",), ("surnames",)]:
        print("--< incorrect tables: {}\n--< check if database file exists".format(tables))
        return False
        
    argv = ["-h"]
    #argv = ["-u", "names.txt"]
    #argv = ["-r"]
    #argv = ["-n", "polish", "-q", "20", "-a", "10"]
    try:
        opts, args = getopt.getopt(argv, "hru:n:s:q:a:")
    except getopt.GetoptError as err:
        print(str(err))
        return False
        
    #parameters at start
    national = "Random"
    sex = "Random"
    quantity = 1
    age = 0
    
    for opt, arg in opts:
        if opt == "-h":
            usage()
            return True
        elif opt in '-r':
            #fully random:
            national = "Random"
            sex = "Random"
            #quantity = 1
            #break
        elif opt in '-u':
            if arg in os.listdir():
                status = sql.update_db(arg)
                if status:
                    print("--< database updated succesfully")
                    return True
                else:
                    print("--< failed to update database")
                    return False
        elif opt in "-n":
            #nationalList = ["english", "polish", "ukrainian"]
            nationalList = sql.data_from_db("names", "national") + sql.data_from_db("surnames", "national")
            nationalList = list(set(nationalList))
            if arg.lower() in nationalList:
                national = arg
            else:
                print("--< wrong nationality choice. Auto choose -> english")
                #national = "english"
        elif opt in "-s":
            if arg.lower() in ("male", "female"):
                sex = arg
            else:
                print("--< wrong sex choice. Auto choose -> male")
        elif opt in "-q":
            if arg.isdigit():
                quantity = int(arg)
            else:
                print("--< put numeric type argument")
        elif opt in "-a":
            if arg.isdigit():
                age = int(arg)
        else:
            usage()
            return True

    #args there: national, sex, quantity, age            

    for x in range(quantity):
        personData = generate_person(national=national, sex=sex, age=age, writeFile=False)
        personData = show_data(personData, 2)
        print("---"*10 + "\n" + personData)

        
        

if __name__ == "__main__":
    global PATH; PATH = script_path()
    main(sys.argv[1:])


'''
18.09.17
maybe we need to use some database
11.02.18
-thats a good idea :)
ehhm
-this script is kind of shit for now
-I am gonna fix it soon

17.02.18
-i need to add zipcode related to address if it exists

22.07.18
-comeback with new ideas :)

how about add:
-flags?
-country on the map?
-fake address?
'''
