import time
import datetime
import random
from dateutil.relativedelta import relativedelta


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

def random_date(start="1-1-1970", end="1-1-1999", format="%d-%m-%Y", prop=random.random()):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def get_age(start):
    today = time.strftime("%d-%m-%Y")
    d1 = datetime.datetime.strptime(start, "%d-%m-%Y")
    d2 = datetime.datetime.strptime(today, "%d-%m-%Y")
    #return abs((d2 - d1).days)
    diffYears = relativedelta(d2, d1).years
    return diffYears

