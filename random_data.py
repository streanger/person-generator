import time
import datetime
import random
from dateutil.relativedelta import relativedelta

def rm_pl_signs(plString):
    plSigns = {'ą':'a', 'ć':'c', 'ę':'e', 'ł':'l', 'ń':'n', 'ó':'o', 'ś':'s', 'ź':'z', 'ż':'z'}
    for key, val in plSigns.items():
        if key in plString:
            plString = plString.replace(key, val)
    return plString

def get_email(personData):
    #make some algoritms
    post = random.choice(["gmail.com", "wp.pl", "o2.pl", "yahoo.com", "hotmail"])
    algoNo = random.randrange(1, 6) + 1
    if algoNo == 1:
        fakeEmail = (personData["Name"]).lower() + "_" + (personData["Surname"]).lower() + "@" + post
    elif algoNo == 2:
        fakeEmail = (personData["Surname"]).lower() + "@" + post   
    elif algoNo == 3:
        fakeEmail = (personData["Surname"]).lower() + (personData["Birthdate"])[-2:] + "@" + post
    elif algoNo == 4:
        fakeEmail = ((personData["Name"]).lower())[0] + (personData["Surname"]).lower() + "@" + post  
    elif algoNo == 5:
        fakeEmail = ((personData["Name"]).lower())[:3] + "_" + ((personData["Surname"]).lower())[0:3] + "@" + post  
    elif algoNo == 6:
        fakeEmail = ((personData["Surname"]).lower())[::-1] + "@" + post
    else:
        fakeEmail = (personData["Name"]).lower() + "_" + (personData["Surname"]).lower() + "@" + post
    return rm_pl_signs(fakeEmail)

def random_date(age=0):
    if not age:
        age = random.randrange(18,51)
    format = "%Y-%m-%d"
    stime = time.mktime(time.strptime(str((datetime.datetime.now() - relativedelta(years=1)).date()), format))
    etime = time.mktime(time.strptime(str(datetime.datetime.now().date()), format))
    ptime = stime + random.random()*(etime - stime)
    randomTime = time.strftime(format, time.localtime(ptime))
    
    date = (datetime.datetime.strptime(randomTime, format) - relativedelta(years=age)).strftime("%d-%m-%Y")
    return date
    
def get_age(start):
    today = time.strftime("%d-%m-%Y")
    d1 = datetime.datetime.strptime(start, "%d-%m-%Y")
    d2 = datetime.datetime.strptime(today, "%d-%m-%Y")
    diffYears = relativedelta(d2, d1).years
    return str(diffYears)

def random_phone():
    firstDigit = random.randrange(1,9)
    phoneNumber = str(firstDigit)
    for x in range(8):
        phoneNumber += str(random.randrange(0,9))
    return "-".join([phoneNumber[x:x+3] for x in range(0, len(phoneNumber), 3)])
    
    
if __name__ == "__main__":
    print("import this rather than use")
    print(random_date())

