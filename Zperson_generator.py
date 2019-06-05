#!/usr/bin/python3
#it would be useful with generate random person data
#11.02.18 -> it still need a lot of work :(
import csv
import os
import getopt
#import logging
import random
import re
import shutil           #download_image
import sys
import tkinter as tk    #gui
import requests         #download_image
from PIL import ImageTk, Image

#own modules
import sqlite_use as sql
from random_data import get_email, random_date, get_age, random_phone
import juster


def download_flags():
    '''download flags and save it to some dir'''
    #just run this function to get flags & countries
    flags_url = "https://www.nationsonline.org"
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

    path = script_path()
    simple_write("countries.txt", "\n".join(countries))     #write countries to .txt

    #write gifs to flags dir
    gifs_dir = "flags"
    if not os.path.exists(gifs_dir):
        os.makedirs(gifs_dir)
    path = os.path.join(path, gifs_dir)
    for gif in gifs:
        gif_url = flags_url + gif
        gif_path = os.path.join(path, gif[7:])               #need to cut gif subpath
        print(gif_url)
        download_image(gif_url, gif_path)
    return gifs, countries
    
    
def download_image(url, file_name="image.png"):
    '''download image from specified url and save it to specified file_name'''
    try:
        response = requests.get(url, stream=True)
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    except:
        pass
    del response
    return True
    
    
def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path
    
    
def simple_write(file, str_content):
    '''simple_write data to .txt file, with specified strContent'''
    with open(file, "w") as f:
        f.write(str_content + "\n")
        f.close()
    return True
    
    
def read_file(file_name, rmnl=False):
    '''read specified file and remove newlines depend on "rmnl" parameter'''
    path = os.path.join(script_path(), file_name)
    try:
        with open(path, "r") as file:
            if rmnl:
                file_content = file.read().splitlines()
            else:
                file_content = file.readlines()
    except:
        file_content = []
    return file_content
    
    
def csv_writer(personList):
    '''write list of data to csv'''
    path = os.path.join(script_path(), "persons.csv")
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for person in personList:
            writer.writerow(person)
        print("--< person data written to csv file")
    return True
    
    
def write_file(file_name, content, endline="\n", over_write=False, response=True):
    '''write file with parameters'''
    if not content:
        return False
    content_type = type(content)
    if content_type in (list, tuple):
        pass
    elif content_type in (int, str):
        content = [str(content)]
    elif content_type is (dict):
        content = list(content.items())
    else:
        return False
    if over_write:
        mode = "w"
    else:
        mode = "a"
    path = os.path.join(script_path(), file_name)
    with open(path, mode) as file:
        for item in content:
            #if rmSign:
            #    for sign in rmSign:
            #        item = (str(item)).replace(sign, "")
            file.writelines(str(item)+endline)
        file.close()
        if response:
            print("--< written to: {0} | content_type: {1}".format(file_name, content_type))
    return True
    
    
def write_names(names):
    '''write names into single files'''
    for key, item in enumerate(names):
        write_file(file_name="name" + str(key) + ".txt", content=item, addNewline=True, over_write=True, subPath="")
    return 0
    
    
def get_data(key, personDictio):
    '''return specified data with using proper functions'''
    if key == "Nationality":
        national_list = sql.data_from_db("names", "national") + sql.data_from_db("surnames", "national")
        national_list = list(set(national_list))
        if not national_list:
            national_list = ["Random"]
        data = random.choice(national_list)
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
    '''iter through dictio parameters and capitalize their values'''
    for key, val in dictio.items():
        if key == "Email":
            continue
        #if type(val) is str:
        if isinstance(val, str):
            dictio[key] = " ".join([item.capitalize() for item in val.split("_")])
    return dictio
    
    
def generate_person(national="Random", sex="Random", age=0):
    '''will generate person data depends on parameters'''
    person_data = {}
    if national == "Random":
        person_data["Nationality"] = get_data("Nationality", person_data)
    else:
        person_data["Nationality"] = national
    if sex == "Random":
        person_data["Sex"] = random.choice(["male", "female"])
    else:
        person_data["Sex"] = sex
    person_data["Birthdate"] = random_date(age=age)
    otherData = ["Name", "Surname", "Age", "Email", "Phone"]
    for key in otherData:
        person_data[key] = get_data(key, person_data)
    person_data = capitalize_dictio(person_data)
    return person_data
    
    
def show_data(dictio, dataType=0):
    '''show data from dictio in different way, depends on dataType'''
    email = "random"
    if dataType == 0:
        email = "\n".join(dictio.values())
    elif dataType == 1:
        email = "\n".join("{}".format(item) for item in dictio.items())
    elif dataType == 2:
        email = "\n".join("{}: {}".format(key, item) for key, item in dictio.items())
    elif dataType == 3:
        email = [dictio["Name"], dictio["Surname"], dictio["Sex"], dictio["Nationality"], dictio["Birthdate"], dictio["Age"], dictio["Email"], dictio["Phone"]]
    elif dataType == 4:
        email = ", ".join(dictio.values())
    else:
        email = "\n".join(dictio.values())
    return email
    
    
class Application(tk.Frame):
    '''gui of person generator'''
    def __init__(self, master, data):
        '''initialize object'''
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
        '''create widgets with initialized data'''
        self.info_phone = tk.Label(text="Phone: {}".format(self.phone)).pack(expand="yes", fill="both", side="bottom")
        self.info_email = tk.Label(text="Email: {}".format(self.email)).pack(expand="yes", fill="both", side="bottom")
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

        #create image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join('images', self.sex + ".png")))
        self.panel = tk.Label(self.root, image=self.image)
        self.panel.pack(side="right")
        
        
def gui_app(person):
    '''gui app of person data'''
    root = tk.Tk()
    root.geometry('{}x{}'.format(600, 500))
    root.resizable(width=False, height=False)
    root.wm_title("zperson")
    app = Application(master=root, data=person)
    app.mainloop()
    
    
def usage():
    '''all parameters of person generator'''
    print("usage:")
    print("-u <fileName> - update db with specified file")
    print("-i <fileName> - interactive update")
    print("-n <nationality> - nationality of person to generate [default=england]")
    print("-s <sex> - gender of person to generate [default=male]")
    print("-q <quantity> - the number of persons(s) to generate [default=1]")
    print("-a <age> - age of person(s)")
    print("-r - random nationality and sex")
    print("-g - gui output")
    print("-l - print list of all nationalities")
    print("-h - this usage help")
    print("--"*35)
    return True
    
    
def get_opt(argv):
    '''get argv and return final options'''
    try:
        opts, arg = getopt.getopt(argv, "hrglu:n:s:q:a:i:")
    except getopt.GetoptError as err:
        print(str(err))
        return False

    #parameters at start
    national = "Random"
    sex = "Random"
    quantity = 1
    age = 0
    gui = False

    for opt, arg in opts:
        if opt in "-h":
            usage()
            return False
        elif opt in '-r':
            national = "Random"
            sex = "Random"
            #quantity = 1
            #break
        elif opt in '-g':
            gui = True
        elif opt in '-l':
            national_list = sql.data_from_db("names", "national") + sql.data_from_db("surnames", "national")
            national_list = [item.lower().replace('_', ' ') for item in national_list]
            national_list = list(set(national_list))
            national_list.sort()
            print("--< list of nationalities:\n{}".format("\n".join(national_list)))
            return False
        elif opt in '-u':
            if arg in os.listdir():
                status = sql.update_db(arg)
                if status:
                    print("--< database updated succesfully")
                else:
                    print("--< failed to update database")
            else:
                print("no such file: '{}'".format(arg))
            return False
        elif opt in '-i':
            #if arg in os.listdir():
            #try:
            if 1:
                status = sql.update_db(arg, interactive=True)
                if status:
                    print("--< database updated succesfully")
                else:
                    raise Exception
            #except:
            else:
                print("--< failed to update database with: '{}'".format(arg))
            return False
        elif opt in "-n":
            #national_list = ["english", "polish", "ukrainian"]
            national_list = sql.data_from_db("names", "national") + sql.data_from_db("surnames", "national")
            national_list = [item.lower().replace('_', ' ') for item in national_list]
            national_list = list(set(national_list))
            if not national_list:
                print("--< empty national list. Please update your database")
                return False
            if arg.lower() in national_list:
                national = arg
            else:
                national = random.choice(national_list)
                print("--< wrong nationality choice. Auto choose -> {}".format(national))
        elif opt in "-s":
            if arg.lower() in ("male", "female"):
                sex = arg
            else:
                sex = random.choice(["male", "female"])
                print("--< wrong sex choice. Random set to: {}".format(sex))
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
    return national, sex, quantity, age, gui
    
    
def main(args):
    '''main function of zperson_generator'''
    
    
    # ***************** check if db exists and *****************
    tables = sql.get_tables("zperson_stuff.db")
    if tables != [("names",), ("surnames",)]:
        print("--< incorrect tables: {}\n--< check if database file exists".format(tables))
        return False
        
        
    # ***************** parse arguments *****************
    correctOpts = get_opt(args)
    if correctOpts:
        #national, sex, quantity, age = get_opt(args)
        national, sex, quantity, age, gui = correctOpts
    else:
        return False
        
        
    personList = [["Name", "Surname", "Sex", "Nationality", "Birthdate", "Age", "Email", "Phone"]]      # header
    
    # ***************** generate persons data *****************
    for _ in range(quantity):
        person_data = generate_person(national=national, sex=sex, age=age)
        show_person = show_data(person_data, 4)     # 2 vs 4
        # print("---"*10 + "\n" + show_person)
        # print(show_person)
        personList.append(show_data(person_data, 3))
    strPersonList = '\n'.join([';'.join(item) for item in personList])
    tableForm = juster.justify(strPersonList)
    print(tableForm)
    # return personList
    
    
    # ***************** write persons data *****************
    csv_writer(personList)              #write data to csv
    
    
    # ***************** show data in gui *****************
    if gui:
        gui_app(person_data)             #to show data and flag, map, photo
    return True
    
    
if __name__ == "__main__":
    PATH = script_path()
    args = sys.argv[1:]
    # args = ['-l']
    args = ['-a', '22', '-n', 'Bangladesh', '-q', '10']
    # args = ['-r', '-a', '22', '-q', '40']
    out = main(args)
    
    
    
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

6.08.18
-much more rubbish than before :)





How the zperson_generaton app works?
    -user puts args in cmd
    -verify parameters and decide what to do
    -generate person(s) data
    -decide how to show data(as text or as gui) and where to store it(.txt or csv)
    -

    
    
    
Values:
    "Name"
    "Surname"
    "Sex"
    "Nationality"
    "Birthdate"
    "Age"
    "Email"
    "Phone"
    
    
    
    
'''


