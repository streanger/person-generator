#!/usr/bin/python3
#it would be useful with generate random person data
#11.02.18 -> it still need a lot of work :(
import os
from datetime import date, timedelta
import datetime
import random
import sys
import shutil   #download_image
import requests #download_image
import getopt
import logging


#own modules
import sqlite_use as sql
from random_data import get_email, random_date, get_age


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

def files_list():
    #return the list of current dir files
    files = os.listdir()
    return files

def get_data_base():
    #read all usefull data from files
    #otherwise use data inside
    return 0

def script_path(fileName=''):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    if fileName:
        fullPath = os.path.join(path, fileName)
        return fullPath
    return path

def get_dir(fileName=""):
    #return our current path
    #if fileName -> return full path
    try:
	    os.chdir(os.path.dirname(__file__))
    except:
	    os.path.dirname(os.path.abspath(__file__))
    pathAbs = os.getcwd()
    logging.info("absolute path:{0}".format(pathAbs))
    if fileName:
        fullPath = pathAbs + "\\" + fileName
        return fullPath
    #path = os.path.join(pathAbs, fileName)
    return pathAbs

def remove_duplicates(someList, sort=True):
    return list(set(someList))

def read_file(fileName, rmnl=False):
    try:
	    os.chdir(os.path.dirname(__file__))
    except:
	    os.path.dirname(os.path.abspath(__file__))
    pathAbs = os.getcwd()
    path = os.path.join(pathAbs, fileName)
    try:
        with open(path, "r") as file:
            if rmnl:
                fileContent = file.read().splitlines()
            else:
                fileContent = file.readlines()
    except:
        fileContent = []
    logging.info("file content:{0}".format(fileContent))
    #print(fileContent)
    return fileContent

def write_file(fileName, content, addNewline=True, overWrite=False, subPath="", response=True):
    if overWrite:
        mode = "w"  #create new file each time
    else:
        mode = "a" #appedn to the file
    #content should be a list
    result = 0
    #is it empty or not
    if not content:
        result = 1
        return result

    #will create subPath
    newpath = os.path.join(get_dir(), subPath)
    path = os.path.join(newpath, fileName)
    #print("path:", path)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    with open(path, mode) as file:
        if addNewline:
            for item in content:
                #print("item:", item)
                file.writelines(str(item)+"\n")
        else:
            for item in content:
                file.writelines(str(item))
        file.close()
        if response:
            print("--< written to: %s" % fileName)
    return result

def random_phone():
    firstDigit = random.randrange(1,9)
    phoneNumber = str(firstDigit)
    for x in range(8):
        phoneNumber += str(random.randrange(0,9))
    return phoneNumber

def write_names(names):
    for key, item in enumerate(names):
        write_file("name" + str(key) + ".txt", item, addNewline=True, overWrite=True, subPath="")
    return 0

def get_data(key, personDictio):
    #return specified data with using proper functions
    #data = "Random"
    if key == "Nationality":
        #data = get_random(read_file("national.txt", rmnl=True))
        data = random.choice(["polish", "english"])
    elif key == "Sex":
        data = random.choice(["Male", "Female"])
    elif key == "Name":
        national = personDictio["Nationality"]
        sex = personDictio["Sex"]
        #fileName = national + sex + ".txt"
        #names read_file(fileName)   #or just use database
        #choose name dependent from national
        data = random.choice(["Kim", "John", "Peter"])
    elif key == "Surname":
        national = personDictio["Nationality"]
        fileName = national + "sunrmaes.txt"
        #surnames = read_file(fileName)  #or go to db
        #choose name dependent from national
        data = random.choice(["Smith", "Johnson", "Kruger"])
    elif key == "Birthdate":
        data = random_date()
    elif key == "Age":
        #data = get_age(personDictio["Birthdate"])[2]
        data = get_age(personDictio["Birthdate"])
    elif key == "Email":
        data = get_email(personDictio)
    elif key == "Phone":
        data = str(random_phone())
    else:
        data = "Random"
    return data

def generate_person(national="Random", sex="Random", writeFile=True):
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
        personData["Sex"] = random.choice(["Male", "Female"])
    else:
        personData["Sex"] = sex
    otherData = ["Name", "Surname", "Birthdate", "Age", "Email", "Phone"]
    for key in otherData:
        personData[key] = get_data(key, personData)
    return personData

def up_db(filename):
    sql.update_db(filename)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hu:n:s:q:")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    quantity = 1
    for opt, arg in opts:
        if opt == "-h":
            print("usage:")
            print("-u <fileName> - file with data to update database")
            print("-n <nationality> - nationality of person to generate [default=english]")
            print("-s <sex> - gender of person to generate [default=male]")
            print("-q <quantity> - the number of persons(s) to generate [default=1]")
            print("---"*8)
        elif opt in '-u':
            if not arg in files_list():
                dbData = ""
            else:
                dbData = arg
            #as an argument put filename; if file not exists return False
        elif opt in "-n":
            nationalList = ["english", "polish", "ukrainian"]
            if not arg.lower() in nationalList:
                print("wrong nationality choice. Auto choose -> english")
                national = "english"
            else:
                national = arg
        elif opt in "-s":
            if not arg.lower() in ("male", "female"):
                print("wrong sex choice. Auto choose -> male")
                sex = "male"
            else:
                sex = arg
        elif opt in "-q":
            if arg.isdigit():
                quantity = int(arg)
            else:
                print("put numeric type argument")
        else:
            help()


    for x in range(quantity):
        personData = generate_person()
        print(x+1, "-->", personData)

    '''
    #this is  just for test
    db, c = sql.update_db()
    data = sql.get_data(db, c, "name", "name", "male")
    print(data)
    return True

    if  ("--dbup" in argv):
        try:
            filename = argv[1]
        except:
            filename = ""
        up_db(filename)
        return True
    else:
        specifiedData = entry_data()
        personData = generate_person(specifiedData = specifiedData)[1]
        print(personData)
    print("exiting...")
    '''

if __name__ == "__main__":
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
'''
