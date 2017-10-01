#it would be useful with generate random person data
import os
from datetime import date, timedelta
import datetime
import random

import shutil   #download_image
import requests #download_image


def download_image(url, fileName="image.png"):
    #will download&save image under specified address
    #url = 'http://ontheedge.hol.es/codeEffects/chooseBg.png'
    try:
        response = requests.get(url, stream=True)
        with open(fileName, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            print("--< image written to: %s" % fileName)
    except:
        print("Wrong url")
    del response
    
def files_list():
    #return the list of current dir files
    files = os.listdir()
    return 

def get_age(birthdate=""):
    
    if birthdate:
        #rounding stuff but should work :)
        birthList = birthdate.split("-")
        dateFormat = datetime.date(day=int(birthList[0]), month=int(birthList[1]), year=int(birthList[2]))
        today = date.today()
        age = (today - dateFormat) // timedelta(days=365.2425)
        return dateFormat, birthdate, age
        
    #random age in defined range (18-50)
    bottomYear = 1967
    topYear = 1999
    start_date = date(day=1, month=1, year=bottomYear).toordinal()
    end_date = date(day=31, month=12, year=topYear).toordinal()
    random_day = date.fromordinal(random.randint(start_date, end_date))
    #just for string 
    day = str(random_day.day)
    month = str(random_day.month)
    year = str(random_day.year)
    random_day_string = day + "-" + month + "-" + year
    #age
    age = (date.today() - random_day) // timedelta(days=365.2425)
    return random_day, random_day_string, age      
    
def get_data_base():
    #read all usefull data from files
    #otherwise use data inside
    return 0

def get_dir(fileName=""):
    #return our current path
    #if fileName -> return full path
    try:
	    os.chdir(os.path.dirname(__file__))
    except:
	    os.path.dirname(os.path.abspath(__file__))
    pathAbs = os.getcwd()
    if fileName:
        fullPath = pathAbs + "\\" + fileName
        return fullPath
    #path = os.path.join(pathAbs, fileName)
    return pathAbs      
    
def remove_duplicates(someList, sort=True):
    #returns list with no duplicates
    if sort:
        someList = list(dict.fromkeys(someList).keys())
        someList.sort()
        return someList
    else:
        return list(dict.fromkeys(someList).keys())
        

    
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
    #print(fileContent)
    return fileContent    
    
def write_file(fileName, content, addNewline=True, overWrite=False, subPath="", response=True):
    if overWrite:
        #create new file each time
        mode = "w"
    else:
        #append to the file
        mode = "a"
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
   
def get_email(personData):
    #make some algoritms
    algoNo = random.randrange(1, 6) + 1
    if algoNo == 1:
        fakeEmail = (personData["Name"]).lower() + "_" + (personData["Surname"]).lower() + "@gmail.com"
    elif algoNo == 2:
        fakeEmail = (personData["Surname"]).lower() + "@gmail.com"    
    elif algoNo == 3:
        fakeEmail = (personData["Surname"]).lower() + (personData["Birthdate"])[-2:] + "@gmail.com"  
    elif algoNo == 4:
        fakeEmail = ((personData["Name"]).lower())[0] + (personData["Surname"]).lower() + "@gmail.com"  
    elif algoNo == 5:
        fakeEmail = ((personData["Name"]).lower())[:3] + "_" + ((personData["Surname"]).lower())[0:3] + "@gmail.com"  
    elif algoNo == 6:
        fakeEmail = ((personData["Surname"]).lower())[::-1] + "@gmail.com"          
    else:
        fakeEmail = (personData["Name"]).lower() + "_" + (personData["Surname"]).lower() + "@gmail.com"
    return fakeEmail
 
def get_data(key, personDictio):
    #return specified data with using proper functions
    data = "Random"
    if key == "Nationality":
        data = get_random(read_file("national.txt", rmnl=True))
    elif key == "Sex":
        data = get_random(["Male", "Female"])
    elif key == "Name":
        #uwaga poprzycinane imiona! skorygowac
        names = (personDictio["Nationality"]).lower() + (personDictio["Sex"]).lower() + "name.txt"
        names = read_file(names, rmnl=True)
        data = get_random(names)
    elif key == "Surname":
        surnames = (personDictio["Nationality"]).lower() + "surname.txt"
        surnames = read_file(surnames, rmnl=True)
        #print(surnames)
        data = get_random(surnames)
        if ((personDictio["Nationality"]).lower() == "polish"):
            if ((personDictio["Sex"]).lower() == "male"):
                return data
            else:
                if data[-1] == "i":
                    return data[:-1] + "a" 
        else:
            return data
    elif key == "Birthdate":
        #think about birth and age 
        data = str(get_age()[1])
    elif key == "Age":
        data = get_age(personDictio["Birthdate"])[2]
    elif key == "Email":
        data = get_email(personDictio)
    elif key == "Phone":
        data = str(random_phone())         
    else:
        data = "Random"
    return data
    
def generate_person(fullyRandom=False, specifiedData = {}, writeFile=True):
    #random dictio data              
    personDataDictio = { "Nationality" : "Random",
                         "Sex" : "Random", 
                         "Name" : "Random", 
                         "Surname" : "Random",
                         "Birthdate" : "Random",
                         "Age" : "Random",
                         "Email" : "Random",
                         "Phone" : "Random"}
    if specifiedData:
        for key, value in specifiedData.items():
            if value == "Random":
                personDataDictio[key] = get_data(key, personDataDictio)
            else:
                #if specified more than one element will choose random of it
                if len(value) > 1:
                    randomValue = get_random(value)
                    personDataDictio[key] = randomValue
                else:
                    personDataDictio[key] = value
    
    #to remember; cant use the same keys
    #dictio = dict(zip(firstList, secondList))    
    #specify some data; leave other as "Random" 
    
    #make list; list help with map object
    personDataList = list(map(list, personDataDictio.items()))
    if writeFile:
        fileName = personDataDictio["Name"].lower() + personDataDictio["Surname"].lower() + ".txt"
        write_file(fileName, personDataList, addNewline=True, overWrite=True, subPath="personData")    
        write_file("AAAllPersonData.txt", personDataList, addNewline=True, overWrite=False, subPath="personData", response=False) #collect all data
        write_file("AAAllPersonData.txt", [30*"-"], addNewline=True, overWrite=False, subPath="personData", response=False) #add separator: ---
     
    #return data as dictio and list both
    return personDataDictio, personDataList

def entry_data():
    specifiedData = { "Nationality" : ["Polish", "English"],
                      "Sex" : "Random", 
                      "Name" : "Random", 
                      #"Surname" : ["Burt", "Roland", "Johnnson"],
                      "Surname" : "Random",
                      "Birthdate" : "Random",
                      "Age" : "Random",
                      "Email" : "Random",
                      "Phone" : "Random"}
                      
    specifiedFull = { "Nationality" : "Polish",
                      "Sex" : "Male", 
                      "Name" : "Steve", 
                      "Surname" : "Johnnson",
                      "Birthdate" : "19.02.1998",
                      "Age" : "19",
                      "Email" : "random@gmail.com",
                      "Phone" : "345876112"}     
    
    return specifiedData
              

def get_random(container):
    #get random element from list
    return random.choice(container)

if __name__ == "__main__":

    #generate random person
    specifiedData = entry_data()
    for x in range(19):
        personData = (generate_person(specifiedData = specifiedData))[1]
        # print(42)

    input("\nenter to exit...\n")

    
  
'''
18.09.17
maybe we need to use some database

for now
age - ok
name - ~

Apart of everything above we could just copy physical data
but this is illegal to use someones personals
you know it :)

'''  
    
    
    
    
    
    
    