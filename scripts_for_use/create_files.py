#create files with names(begin) and content
import os
import sys

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

def simple_write(file, strContent):
    with open(file, "w") as f:
        f.write(strContent + "\n")
        f.close()
    return True    
    
def main(filesList, content):
    path = script_path()
    appendix = ".txt"
    for file in filesList:
        filePath = os.path.join(path, file + "_" + content + appendix)
        fileContent = content + "," + file
        simple_write(filePath, fileContent)
        print("file written to : {}".format(filePath))
    return True

    
if __name__ == "__main__":
    filesList = ["Bangladesh", "Cambodia", "China", "Georgia", "India", "Indonesia", "Israel", "Japan", "Korea", "Nepal",
                 "Philippines", "Sri Lanka", "Taiwan", "Thailand", "Vietnam"]   #asia
    filesList = ["Canada", "Costa Rica", "Cuba", "Dominican Republic", "El Salvador", "Guatemala", "Mexico", "USA", "Texas"]    #north america
    filesList = ["Argentina", "Brazil", "Chile", "Colombia", "Paraguay", "Suriname"]    #south america
    filesList = ["Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina",
                 "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Faroe Islands", "Finland",
                 "France", "Georgia", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Kosovo", "Latvia",
                 "Lithuania", "Luxembourg", "Malta", "Macedonia", "Moldova", "Netherlands", "Norway", "Poland",
                 "Portugal", "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain", "Canary Islands", "Sweden",
                 "Switzerland", "Turkey", "Ukraine", "United Kingdom", "United Kingdom"]  #europe
    filesList = ['Nigeria', 'Ethiopia', 'Egypt', 'Democratic Republic of the Congo', 'South Africa', 'Tanzania', 'Kenya', 'Sudan', 'Algeria', 'Uganda',
                 'Morocco', 'Mozambique', 'Ghana', 'Angola', 'Ivory Coast', 'Madagascar', 'Cameroon', 'Niger', 'Burkina Faso', 'Mali',
                 'Malawi', 'Zambia', 'Somalia', 'Senegal', 'Chad', 'Zimbabwe', 'South Sudan', 'Rwanda', 'Tunisia', 'Guinea', 'Benin',
                 'Burundi', 'Togo', 'Eritrea', 'Sierra Leone', 'Libya', 'Republic of the Congo', 'Central African Republic', 'Liberia', 'Mauritania', 'Namibia',
                 'Botswana', 'Gambia', 'Equatorial Guinea', 'Lesotho', 'Gabon', 'Guinea-Bissau', 'Mauritius', 'Swaziland', 'Djibouti',
                 'Réunion', 'Comoros', 'Cape', 'Western Sahara', 'Mayotte', 'Sao Tomé and Príncipe', 'Seychelles', 'Saint Helena']  #africa
    #filesList = []  #empty list to not write a rubbish stuff all around
    filesList = [item.lower().replace(" ", "_") for item in filesList]
    #content = "surnames"
    content = "names"
    main(filesList, content)
    