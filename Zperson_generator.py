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
import csv
import re

#own modules
import sqlite_use as sql
from random_data import get_email, random_date, get_age, random_phone

#gui
import tkinter as tk
from PIL import ImageTk, Image


def download_flags():
    #just run this function to get flags & countries
    flagsUrl = "https://www.nationsonline.org"
    urls = ["https://www.nationsonline.org/oneworld/flags_of_africa.htm",
            "https://www.nationsonline.org/oneworld/flags_of_the_americas.htm",
            "https://www.nationsonline.org/oneworld/flags_of_asia.htm",
            "https://www.nationsonline.org/oneworld/flags_of_australia_oceania.htm",
            "https://www.nationsonline.org/oneworld/flags_of_europe.htm"]
    gifs = []
    for url in urls:
        res = requests.get(url)
        content = res.text
        gifs.extend(re.findall(r'[\/][\S]+flag.gif', content))
    gifs = list(set(gifs))
    countries = [item[7:-9].lower() for item in gifs]
    countries.sort()        #in place
    
    #write countries to .txt
    path = script_path()
    simple_write("countries.txt", "\n".join(countries))
    
    #write gifs to flags dir
    gifsDir = "flags"
    if not os.path.exists(gifsDir):
        os.makedirs(gifsDir)
    path = os.path.join(path, gifsDir)
    for gif in gifs:
        gifUrl = flagsUrl + gif
        gifPath = os.path.join(path, gif[7:])       #need to cut gif subpath
        print(gifUrl)
        download_image(gifUrl, gifPath)
    return gifs, countries

def download_image(url, fileName="image.png"):
    try:
        response = requests.get(url, stream=True)
        with open(fileName, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    except:
        pass
    del response
    return True
    
def script_path(fileName=''):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    if fileName:
        fullPath = os.path.join(path, fileName)
        return fullPath
    return path

def remove_duplicates(someList, sort=True):
    return list(set(someList))

def simple_write(file, strContent):
    with open(file, "w") as f:
        f.write(strContent + "\n")
        f.close()
    return True    
    
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

def csv_writer(personList):
    path = os.path.join(PATH, "persons.csv")
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for person in personList:
            writer.writerow(person)
        print("--< person data written to csv file")
    return True
    
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
    print("-u <fileName> - update db with specified file")
    print("-i <fileName> - interactive update")
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
    elif dataType == 3:
        return [dictio["Name"], dictio["Surname"], dictio["Sex"], dictio["Nationality"], dictio["Birthdate"], dictio["Age"], dictio["Email"], dictio["Phone"]]
    else:
        return "\n".join(dictio.values())

class Application(tk.Frame):
    def __init__(self, master=None, data=[]):
        super().__init__(master)
        self.pack()
        self.data = data
        self.sex = data["Sex"]
        self.name = data["Name"]
        self.surname = data["Surname"]
        self.birth = data["Birthdate"]
        self.natio = data["Nationality"]
        self.age = data["Age"]
        self.email = data["Email"]
        self.phone = data["Phone"]
        self.root = master
        self.create_widgets()

    def create_widgets(self):     
        self.info_phone = tk.Label(text="Phone: {}".format(self.phone)).pack(expand="yes", fill="both", side="bottom")     
        self.info_email = tk.Label(text="Mail: {}".format(self.email)).pack(expand="yes", fill="both", side="bottom")
        self.info_age = tk.Label(text="Age: {}".format(self.age)).pack(expand="yes", fill="both", side="bottom")
        self.info_birth = tk.Label(text="Birthdate: {}".format(self.birth)).pack(expand="yes", fill="both", side="bottom")
        self.info_sex = tk.Label(text="Sex: {}".format(self.sex)).pack(expand="yes", fill="both", side="bottom")
        self.info_natio = tk.Label(text="Nationality: {}".format(self.natio)).pack(expand="yes", fill="both", side="bottom")
        self.info_surname = tk.Label(text="Surname: {}".format(self.surname)).pack(expand="yes", fill="both", side="bottom")
        self.info_name = tk.Label(text="Name: {}".format(self.name)).pack(expand="yes", fill="both", side="bottom")

        self.save = tk.Button(self)
        self.save["text"] = "OK"
        self.save["fg"] = "green"
        #self.save["command"] = self.save_data
        self.save.pack(side="left")

        self.read = tk.Button(self)
        self.read["text"] = "Next"
        self.read["fg"] = "green"
        #self.read["command"] = self.get_post_by_date
        self.read.pack(side="left")        

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.root.destroy).pack(side="left")        
        
        
        '''
        self.scroll = tk.Scrollbar(self)    #self instead of root - it matters
        self.text = tk.Text(self, height=20, width=20)
        self.scroll.pack(side="left", fill=tk.Y)
        self.text.pack()
        self.scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)
        '''
        
        #create image
        self.image = ImageTk.PhotoImage(Image.open(self.sex + ".png"))    
        self.panel = tk.Label(self.root, image=self.image)
        self.panel.pack(side = "right")
        
        
def gui_app(person):        
    root = tk.Tk()
    root.geometry('{}x{}'.format(500, 400))
    root.resizable(width=False, height=False)
    root.wm_title("zperson")
    app = Application(master=root, data=person)
    app.mainloop()

def get_opt(argv):
    try:
        opts, args = getopt.getopt(argv, "hru:n:s:q:a:i:")
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
            return False
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
                    return False
                else:
                    print("--< failed to update database")
                    return False
            else:
                print("no such file: '{}'".format(arg))
                return False
        elif opt in '-i':
            #if arg in os.listdir():
            try:
                status = sql.update_db(arg, interactive=True)
                if status:
                    print("--< database updated succesfully")
                    return False
                else:
                    print("--< failed to update database")
                    return False
            #else:
            except:
                print("no such file: '{}'".format(arg))
                return False
        elif opt in "-n":
            #nationalList = ["english", "polish", "ukrainian"]
            nationalList = sql.data_from_db("names", "national") + sql.data_from_db("surnames", "national")
            nationalList = list(set(nationalList))
            if not nationalList:
                print("--< empty national list. Please update your database")
                return False
            if arg.lower() in nationalList:
                national = arg
            else:
                national = random.choice(nationalList)
                print("--< wrong nationality choice. Auto choose -> {}".format(national))
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
            return False
    return national, sex, quantity, age
    
def main(argv):
    #check if db exists and
    tables = sql.get_tables("zperson_stuff.db")
    if tables != [("names",), ("surnames",)]:
        print("--< incorrect tables: {}\n--< check if database file exists".format(tables))
        return False
        
    #argv = ["-h"]
    #argv = ["-u", "names.txt"]
    #argv = ["-r", "-q", "99", "-a", "25"]
    #argv = ["-n", "polish", "-q", "3", "-a", "22"]

    correctOpts = get_opt(argv)
    if correctOpts:
        #national, sex, quantity, age = get_opt(argv)
        national, sex, quantity, age = correctOpts
    else:
        return False

    personList = [["Name", "Surname", "Sex", "Nationality", "Birthdate", "Age", "Email", "Phone"]]
    for x in range(quantity):
        personData = generate_person(national=national, sex=sex, age=age, writeFile=False)
        showPerson = show_data(personData, 2)
        print("---"*10 + "\n" + showPerson)        
        personList.append(show_data(personData, 3))

        
    #write data to csv
    csv_writer(personList)
    gui_app(personData)           #to show data and flag, map, photo 

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
-flags? (+-)
-country on the map?
-fake address?

todo:
-usuniecie duplikatow z bazy danych
-weryfikacja obecnosci rekordu przed zapisem
-gui wraz ze zdjęciem(schematyczne-płeć, bądź prawdzie), flagą, oraz mapką kraju pochodzenia

30.07.18
to_do:
-need to add africa surnames and names for all continents
'''
