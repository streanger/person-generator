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
